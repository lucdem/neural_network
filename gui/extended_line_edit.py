from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal


class Extended_QLineEdit(QLineEdit):
	edit_finished_value_signal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.editingFinished.connect(self.__edit_finished_handler)

	def __edit_finished_handler(self):
		self.edit_finished_value_signal.emit(self.text())