from tkinter.messagebox import NO
from typing import Optional

from PyQt5.QtGui import QFont, QFontMetrics


def get_text_width(text: str, font: Optional[QFont] = None):
	if font is None:
		font = QFont()
	font_metrics = QFontMetrics(font)
	return font_metrics.horizontalAdvance(text)