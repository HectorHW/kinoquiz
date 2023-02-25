import pydantic
import yaml
from pydantic import BaseModel


class BaseQuestion(BaseModel, extra="forbid"):
    cost: int
    prompt: str
    answer: str
    answer_image: str | None = None
    time: int = 20
    answer_time: int = 12
    done: bool = False


class VideoQuestion(BaseQuestion, extra="forbid"):
    video: str


class ImageQuestion(BaseQuestion, extra="forbid"):
    image: str


class MusicQuestion(BaseQuestion, extra="forbid"):
    audio: str


class TextQuestion(BaseQuestion, extra="forbid"):
    pass


AnyQuestion = VideoQuestion | ImageQuestion | MusicQuestion | TextQuestion


class Category(BaseModel, extra="forbid"):
    name: str
    items: list[AnyQuestion]
    fontsize: int = 48


class Section(BaseModel, extra="forbid"):
    categories: list[Category]


Game = list[Section]


def parse_file(filename: str) -> Game:
    with open(filename) as f:
        yml = yaml.safe_load(f)
        print(yml)
        return pydantic.parse_obj_as(Game, yml)


class State(BaseModel, extra="forbid"):
    game: Game
    CURRENT_SECTION: int = 0
    CURRENT_QUESTION: AnyQuestion | None = None
