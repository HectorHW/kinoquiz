from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from entities import (
    parse_file,
    Game,
    Section,
    ImageQuestion,
    MusicQuestion,
    VideoQuestion,
    AnyQuestion,
)

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
import textwrap
from svoja.timer import ControllableTimer

Window.size = (1920, 1080)

grid_vsize = 1080 // 6 - 3


class State:
    current_question: AnyQuestion = None  # type: ignore


def center(item, **args):
    layout = AnchorLayout(**args)
    # container = BoxLayout()
    # container.add_widget(item)
    layout.add_widget(item)
    return layout


def ratio_sized(item, x: float = 1.0, y: float = 1.0):
    layout = BoxLayout(size_hint=(x, y))
    layout.add_widget(item)
    return layout


def pad(item, pad_px: int | tuple[int, int] = 0):
    layout = AnchorLayout(padding=pad_px)
    layout.add_widget(item)
    return layout


class GridButton(Button):
    def __init__(self, text: str, callback, **kwargs):
        super().__init__(
            size_hint=(None, None),
            size=(int(grid_vsize * 1.2), grid_vsize),
            text=text,
            halign="center",
            valign="center",
            font_size=75,
            **kwargs,
        )
        self.bind(on_press=callback)  # type: ignore


class GridLabel(Label):
    def __init__(self, text: str, font_size: int = 48, **kwargs):
        h_size = int(grid_vsize * 2.6)
        chars_in_row = h_size // font_size
        text = "\n".join(
            textwrap.wrap(text, width=chars_in_row, break_long_words=False)
        )

        super().__init__(
            size_hint=(None, None),
            size=(h_size, grid_vsize),
            text=text,
            text_size=(h_size - 20, None),
            halign="center",
            valign="center",
            font_size=font_size,
            **kwargs,
        )


class UIButton(Button):
    def __init__(self, text: str, callback, **kwargs):
        super().__init__(
            size_hint=(None, None),
            size=(200, 160),
            text=text,
            halign="center",
            valign="center",
            font_size=55,
            **kwargs,
        )
        self.bind(on_press=callback)  # type: ignore


class GridScreen(Screen):
    def __init__(self, section: Section, **kw):
        super().__init__(**kw)
        grid = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            size_hint_y=None,
        )
        grid_height = 0
        grid_width = 0
        for category in section.categories:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                size_hint_y=1,
            )
            row.add_widget(GridLabel(text=category.name, font_size=category.fontsize))

            for question in category.items:
                q_btn = GridButton(
                    text=str(question.cost),
                    callback=partial(self.click_question, question=question),
                )
                row.add_widget(q_btn)

            grid.add_widget(row)
            grid_height += grid_vsize
            grid_width = row.width

        grid.height = grid_height
        grid.minimum_height = grid_height
        grid.width = grid_width
        grid.minimum_width = grid_width

        self.add_widget(pad(center(grid, anchor_x="left"), 80))

    def click_question(self, instance, *, question):
        question.done = True

        instance.set_disabled(True)
        State.current_question = question

        if isinstance(question, VideoQuestion):
            video.set_video(question.video)
            video.question = question.prompt
            self.manager.current = "video_question"
        elif isinstance(question, ImageQuestion):
            image.set_image(question.image)
            self.manager.current = "image_question"
        elif isinstance(question, MusicQuestion):
            raise NotImplementedError
        else:
            text.question = question.prompt
            self.manager.current = "text_question"


class QuestionScreen(Screen):
    def __init__(self, top_widget=None, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="horizontal")

        self.timer = ControllableTimer(duration=15)

        self.layout.add_widget(
            ratio_sized(center(UIButton(text="back", callback=self.back)), x=0.2)
        )

        q_screen = BoxLayout(orientation="vertical")

        self.q_text = Label(text="question", font_size=40)

        if top_widget is not None:
            q_screen.add_widget(ratio_sized(top_widget, y=0.7))
            q_screen.add_widget(ratio_sized(self.q_text, y=0.3))
        else:
            q_screen.add_widget(self.q_text)

        q_screen.add_widget(ratio_sized(self.timer, y=0.05))

        # TODO timer
        self.layout.add_widget(ratio_sized(q_screen, x=0.8))

        self.add_widget(self.layout)

    def back(self, *args):
        self.timer.inner.pause()
        self.manager.current = "grid"

    def on_enter(self):
        self.timer.inner.duration = State.current_question.time
        self.timer.inner.restart()

    @property
    def question(self) -> str:
        return self.q_text.text

    @question.setter
    def question(self, value: str):
        self.q_text.text = value


class VideoQuestionScreen(QuestionScreen):
    def __init__(self, **kw):
        self.player = VideoPlayer(size=(800, 480))
        super().__init__(top_widget=self.player, **kw)

    def set_video(self, video: str):
        print("set video to", video)
        self.player.source = video

    def back(self, *args):
        self.player.state = "stop"
        super().back()

    def on_enter(self):
        self.player.state = "play"
        super().on_enter()


video = VideoQuestionScreen(name="video_question")


class TextQuestionScreen(QuestionScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def back(self, *args):
        self.manager.current = "grid"


text = TextQuestionScreen(name="text_question")


class ImageQuestionScreen(QuestionScreen):
    def __init__(self, **kw):
        self.image = Image(size=(800, 480))

        super().__init__(top_widget=self.image, **kw)

    def set_image(self, image: str):
        self.image.source = image


image = ImageQuestionScreen(name="image_question")


class GameManager(ScreenManager):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self.game: Game = game


class SI(App):
    def build(self):
        game = parse_file("game.yaml")
        sm = GameManager(game=game, transition=FadeTransition())
        sm.add_widget(GridScreen(name="grid", section=game.sections[0]))

        sm.add_widget(video)
        sm.add_widget(text)
        sm.add_widget(image)
        Window.fullscreen = "auto"
        return sm


if __name__ == "__main__":
    print()
    SI().run()
