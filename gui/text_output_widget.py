from PyQt5.QtWidgets import QPlainTextEdit


class TextOutputWidget(QPlainTextEdit):
	def __init__(self):
		super().__init__()
		self.setReadOnly(True)
		for i in range(100):
			self.message("hello")
		self.setBackgroundVisible(False)

	def message(self, string):
		self.appendPlainText(string)