from functools import partial

from entities import ImageQuestion, MusicQuestion, State, VideoQuestion
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer

from kinoquiz.buttons import GRID_VSIZE, GridButton, GridLabel, UIButton
from kinoquiz.layout import center, pad, ratio_sized
from kinoquiz.timer import ControllableTimer


class GridScreen(Screen):
    def __init__(self, state: State, **kw):
        super().__init__(**kw)
        grid = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            size_hint_y=None,
        )
        self.state = state
        grid_height = 0
        grid_width = 0
        for category in self.state.CURRENT_SECTION.categories:  # type: ignore
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
            grid_height += GRID_VSIZE
            grid_width = row.width

        grid.height = grid_height
        grid.minimum_height = grid_height
        grid.width = grid_width
        grid.minimum_width = grid_width

        self.add_widget(pad(center(grid, anchor_x="left"), 80))

    def click_question(self, instance, *, question):
        question.done = True

        instance.set_disabled(True)
        self.state.CURRENT_QUESTION = question

        if isinstance(question, VideoQuestion):
            self.manager.current = "video_question"
        elif isinstance(question, ImageQuestion):
            self.manager.current = "image_question"
        elif isinstance(question, MusicQuestion):
            raise NotImplementedError
        else:
            self.manager.current = "text_question"


class QuestionScreen(Screen):
    def __init__(self, state: State, top_widget=None, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="horizontal")
        self.state = state
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
        self.manager.current = "grid"

    def on_pre_enter(self, *args):
        self.timer.inner.duration = self.state.CURRENT_QUESTION.time  # type: ignore
        self.timer.inner.reset()
        self.q_text.text = self.state.CURRENT_QUESTION.prompt  # type: ignore

    def on_enter(self):
        self.timer.inner.restart()

    def on_leave(self, *args):
        self.timer.inner.pause()
        return super().on_leave(*args)

    @property
    def question(self) -> str:
        return self.q_text.text

    @question.setter
    def question(self, value: str):
        self.q_text.text = value


class VideoQuestionScreen(QuestionScreen):
    def __init__(self, state: State, **kw):
        self.player = VideoPlayer(size=(800, 480))
        super().__init__(top_widget=self.player, state=state, **kw)

    def on_pre_enter(self, *args):
        self.player.source = self.state.CURRENT_QUESTION.video  # type: ignore
        return super().on_pre_enter(*args)

    def on_enter(self):
        self.player.state = "play"
        return super().on_enter()

    def on_leave(self, *args):
        self.player.state = "stop"
        return super().on_leave(*args)


class TextQuestionScreen(QuestionScreen):
    def __init__(self, state: State, **kw):
        super().__init__(state=state, **kw)


class ImageQuestionScreen(QuestionScreen):
    def __init__(self, state: State, **kw):
        self.image = Image(size=(800, 480))

        super().__init__(top_widget=self.image, state=state, **kw)

    def on_enter(self):
        return super().on_enter()

    def on_pre_enter(self, *args):
        self.image.source = self.state.CURRENT_QUESTION.image  # type: ignore
        return super().on_pre_enter(*args)
