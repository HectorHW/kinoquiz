import pydantic
import yaml
from pydantic import BaseModel


class BaseQuestion(BaseModel):
    cost: int
    prompt: str
    answer: str
    answer_image: str | None = None
    time: int = 20
    done: bool = False


class VideoQuestion(BaseQuestion):
    video: str


class ImageQuestion(BaseQuestion):
    image: str


class MusicQuestion(BaseQuestion):
    audio: str


class TextQuestion(BaseQuestion, extra="forbid"):
    pass


AnyQuestion = VideoQuestion | ImageQuestion | MusicQuestion | TextQuestion


class Category(BaseModel):
    name: str
    items: list[AnyQuestion]
    fontsize: int = 48


class Section(BaseModel):
    categories: list[Category]


Game = list[Section]


def parse_file(filename: str) -> Game:
    with open(filename) as f:
        yml = yaml.safe_load(f)
        print(yml)
        return pydantic.parse_obj_as(Game, yml)


class State(BaseModel):
    game: Game
    CURRENT_SECTION: int = 0
    CURRENT_QUESTION: AnyQuestion | None = None
