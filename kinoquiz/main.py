from entities import (
    Game,
    State,
    parse_file,
)
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition, ScreenManager

from kinoquiz.screens import (
    GridScreen,
    ImageQuestionScreen,
    TextQuestionScreen,
    VideoQuestionScreen,
    ImageAnswerScreen,
    TextAnswerScreen,
)

Window.size = (1920, 1080)

grid_vsize = 1080 // 6 - 3


state = State()


class GameManager(ScreenManager):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self.game: Game = game


class SI(App):
    def build(self):
        game = parse_file("game.yaml")
        sm = GameManager(game=game, transition=FadeTransition())
        state.CURRENT_SECTION = game.sections[0]

        grid = GridScreen(name="grid", state=state)

        image = ImageQuestionScreen(name="image_question", state=state)
        video = VideoQuestionScreen(name="video_question", state=state)
        text = TextQuestionScreen(name="text_question", state=state)

        image_answer = ImageAnswerScreen(name="image_answer", state=state)
        text_answer = TextAnswerScreen(name="text_answer", state=state)

        sm.add_widget(grid)

        sm.add_widget(video)
        sm.add_widget(text)
        sm.add_widget(image)
        sm.add_widget(image_answer)
        sm.add_widget(text_answer)
        Window.fullscreen = "auto"
        return sm


if __name__ == "__main__":
    print()
    SI().run()
