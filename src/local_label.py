"""自己写的一些 label."""

from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING

from pyglet.text.document import FormattedDocument
from pyglet.text import DocumentLabel, AnchorX, AnchorY

if TYPE_CHECKING:
    from pyglet.graphics import Batch, Group


class IconLabel(DocumentLabel):
    """用来显示 icon 的 Label."""

    def __init__(
        self,
        text: str = "",
        text_font: str = "Arial",
        icon_font: str = "Segoe Fluent Icons",
        font_size: float = 12,
        filter_func: Callable[[str], list[bool]] | None = None,
        bold: bool = False,
        italic: bool = False,
        stretch: bool = False,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        x: int = 0,
        y: int = 0,
        z: int = 0,
        width: int | None = None,
        height: int | None = None,
        anchor_x: AnchorX = "left",
        anchor_y: AnchorY = "baseline",
        rotation: int = 0,
        align: str = "left",
        multiline: bool = False,
        dpi: int = 96,
        batch: Batch | None = None,
        group: Group | None = None,
        program: Any = None,
    ) -> None:
        """创建一个带 fallback font 的 Label."""
        self._text = text
        self.filter_func = filter_func or self.filter_text
        self.text_font = text_font
        self.icon_font = icon_font
        self.stretch = stretch
        self.align = align

        doc = self.decode_text(text)  # 解码文本
        super().__init__(
            doc,
            x,
            y,
            z,
            width,
            height,
            anchor_x,
            anchor_y,
            rotation,
            multiline,
            dpi,
            batch,
            group,
            program,
            init_document=False,
        )

        self.document.set_style(
            0,
            len(text),
            {
                "font_size": font_size,
                "bold": bold,
                "italic": italic,
                "stretch": stretch,
                "color": color,
                "align": align,
            },
        )

    @staticmethod
    def filter_text(texts: str) -> list[bool]:
        """过滤一遍输入中的字符, 属于 icon 的给 true, 不属于的给 false.
        Segoe Fluent Icons 的 Icon 范围: E000-F800.
        """
        return [
            (ord(text) >= 0xE000 and ord(text) <= 0xF800 and text != " ")  # noqa: PLR2004
            for text in texts
        ]

    def decode_text(self, text: str) -> FormattedDocument:
        """解码文本."""
        doc = FormattedDocument()
        doc.text = text  # 初始化
        # 过滤处理部分
        # 先全部设置为 icon font
        doc.set_style(0, len(text), {"font_name": self.icon_font})
        # 再根据 filter_func 过滤出需要设置为 text font 的部分
        enables = [value[0] for value in enumerate(self.filter_func(text)) if not value[1]]
        for index in enables:
            doc.set_style(index, index + 1, {"font_name": self.text_font})

        return doc

    def set_color_on_text_pos(self, pos: int, color: tuple[int, int, int, int]) -> None:
        """设置文本中的某个位置的颜色."""
        self.document.set_style(pos, pos + 1, {"color": color})

    @property
    def text(self) -> str:
        """返回 Label 的文本内容."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """设置 Label 的文本内容."""
        assert isinstance(value, str), "value must be a string"
        self._text = value
        self.document = self.decode_text(value)
