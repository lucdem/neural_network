from PyQt5.QtWidgets import QPlainTextEdit


class TextOutputWidget(QPlainTextEdit):
	def __init__(self):
		super().__init__()
		self.setReadOnly(True)
		self.setBackgroundVisible(False)

	def message(self, msg: str, **kwargs):
		if len(kwargs) > 0:
			msg += f' ### {kwargs}'
		self.appendPlainText(msg)