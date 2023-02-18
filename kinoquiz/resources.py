from kinoquiz.entities import parse_file, Game, Section, Category, AnyQuestion
import os
import urllib.request
from hashlib import sha1


def get_base_dir() -> str:
    return os.environ.get("GAME_DIR", ".")


def get_game():
    game = parse_file(os.path.join(get_base_dir(), "game.yaml"))
    fix_game(game)
    return game


def fix_game(game):
    for section in game:
        fix_section(section)


def fix_section(section: Section):
    for category in section.categories:
        fix_category(category)


def fix_category(category: Category):
    for question in category.items:
        fix_question(question)


def download_resource(url: str):
    if not url.startswith("http"):
        return url
    hashcode = sha1(url.encode()).hexdigest()
    extension = url.rsplit(".", maxsplit=1)[-1]
    new_name = f"{hashcode}.{extension}"
    urllib.request.urlretrieve(url, new_name)
    return new_name


def fix_question(question: AnyQuestion):
    if question.answer_image is not None:
        question.answer_image = download_resource(question.answer_image)

    if hasattr(question, "image"):
        question.image = download_resource(question.image)  # type: ignore

    if hasattr(question, "video"):
        question.video = download_resource(question.video)  # type: ignore
