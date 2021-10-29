from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

from .load_file_widget import LoadFileWidget


class DataSetBox(QGroupBox):
	def __init__(self, title):
		super().__init__()

		self.setTitle(title)
		self.setLayout(QVBoxLayout())
		self.layout().addWidget(LoadFileWidget())