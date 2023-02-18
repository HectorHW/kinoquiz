from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout


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
