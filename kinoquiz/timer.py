from contextlib import suppress

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Timer(Label):
    def __init__(self, duration=1, update_interval: float = 1 / 30, **kwargs):
        super().__init__(**kwargs)
        self.height = 30

        self.duration = duration

        self.progress = duration
        self.running = False
        self.update_interval = update_interval
        Clock.schedule_interval(lambda _: self.tick(), update_interval)

    def tick(self):
        if not self.running:
            return
        if self.progress == 0:
            return
        self.progress = max(0, self.progress - self.update_interval)
        self.update()

    @property
    def percent_progress(self):
        return getattr(self, "progress", 1) / getattr(self, "duration", 1)

    def update(self):
        self.canvas.clear()  # type: ignore
        with self.canvas:  # type: ignore
            Color(0.1, 0.4, 1, 0.6)
            Rectangle(
                pos=self.pos,
                size=(self.width * self.percent_progress, self.height),
            )
            Color(0, 0, 1, 0.1)
            Rectangle(
                pos=(self.x + self.width * self.percent_progress, self.y),
                size=(self.width * (1 - self.percent_progress), self.height),
            )

    def on_size(self, *args):
        self.update()

    def reset(self):
        self.progress = self.duration
        self.running = False
        self.update()

    def restart(self):
        self.progress = self.duration
        self.running = True
        self.update()

    def pause(self):
        self.running = False
        self.update()

    def resume(self):
        self.running = True
        self.update()

    def trigger(self):
        print("trigger")
        if self.running:
            self.pause()
        else:
            self.resume()


class ControllableTimer(BoxLayout):
    def __init__(self, duration=1, update_interval: float = 1 / 30, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.stop = Button(text="||", height=30, width=30, size_hint=(None, None))
        self.inner = Timer(duration=duration, update_interval=update_interval)
        self.stop.bind(on_press=lambda _: self.inner.trigger())  # type: ignore
        self.add_widget(self.stop)
        self.add_widget(self.inner)

    def on_size(self, *args):
        with suppress(NameError):
            self.stop.width = self.height
            self.stop.height = self.height
