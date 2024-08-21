"""pyme 的用户登录 UI 重写版本."""

from __future__ import annotations

from pathlib import Path

import pyglet

from pyglet.window import Window
from pyglet.graphics import Batch, Group
from pyglet.gl import glClearColor

from .local_label import IconLabel


class LoginWindow(Window):
    """主窗口."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self.main_batch = Batch()
        self.main_group = Group()

        self.lang_label = IconLabel(
            x=20,
            y=200,
            font_size=24,
            # text_font="Segoe Fluent Icons",
            text="\ue88b \ue88c \ue88d \ue985 \ue97e",
            batch=self.main_batch,
            group=self.main_group,
        )
        self.lang_label.set_color_on_text_pos(0, (255, 255, 205, 255))

        # 16、20、24、32、40、48 64
        self.test_label = IconLabel(
            x=20,
            y=20,
            font_size=20,
            text="\ue003 \ue005 \ue0a2 \uf7b5 \ue971 \ue972 \ue973 \ue974",
            batch=self.main_batch,
            group=self.main_group,
        )

        self.icon_label = IconLabel(
            x=20,
            y=100,
            text_font="HarmonyOS Sans SC",
            text="Hello, World! \ue700 \ue701 \ue702 \ue703 \ue704 \ue705 \ue706",
            color=(255, 255, 255, 255),
            batch=self.main_batch,
            group=self.main_group,
        )

    def on_draw(self) -> None:
        self.clear()
        self.main_batch.draw()

    def start(self) -> None:
        glClearColor(34 / 255, 34 / 255, 34 / 255, 1)
        pyglet.app.run(interval=1 / 30)

def start_func() -> None:
    # 加载字体文件
    font_path = Path("./fonts")
    for font_file in font_path.glob("*.ttf"):
        pyglet.font.add_file(str(font_file))

    window = LoginWindow(width=600, height=300, caption="Login")
    window.start()


__all__ = ["start_func"]
