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
from kinoquiz.resources import get_game

Window.size = (1920, 1080)

grid_vsize = 1080 // 6 - 3


class GameManager(ScreenManager):
    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self.game: Game = game


class SI(App):
    def build(self):
        game = get_game()
        print(game)
        sm = GameManager(game=game, transition=FadeTransition())
        state = State(game=game)

        for i, section in enumerate(game):
            sec_name = f"grid_{i}"
            grid = GridScreen(name=sec_name, state=state, section=section)
            sm.add_widget(grid)

        image = ImageQuestionScreen(name="image_question", state=state)
        video = VideoQuestionScreen(name="video_question", state=state)
        text = TextQuestionScreen(name="text_question", state=state)

        image_answer = ImageAnswerScreen(name="image_answer", state=state)
        text_answer = TextAnswerScreen(name="text_answer", state=state)

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
