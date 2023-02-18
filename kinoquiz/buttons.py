import textwrap

from kivy.uix.button import Button
from kivy.uix.label import Label

GRID_VSIZE = 1080 // 6 - 3


class GridButton(Button):
    def __init__(self, text: str, callback, **kwargs):
        super().__init__(
            size_hint=(None, None),
            size=(int(GRID_VSIZE * 1.2), GRID_VSIZE),
            text=text,
            halign="center",
            valign="center",
            font_size=75,
            **kwargs,
        )
        self.bind(on_press=callback)  # type: ignore


class GridLabel(Label):
    def __init__(self, text: str, font_size: int = 48, **kwargs):
        h_size = int(GRID_VSIZE * 2.6)
        chars_in_row = h_size // font_size
        text = "\n".join(
            textwrap.wrap(text, width=chars_in_row, break_long_words=False)
        )

        super().__init__(
            size_hint=(None, None),
            size=(h_size, GRID_VSIZE),
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
