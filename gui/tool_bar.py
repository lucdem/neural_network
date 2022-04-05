from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import pyqtSignal


class ToolBar(QToolBar):
	def __init__(self, title: str) -> None:
		super().__init__(title)
		self.options_action = QAction(QIcon("gui/icons/gear.svg"), 'Options')
		self.addAction(self.options_action)
		self.show()