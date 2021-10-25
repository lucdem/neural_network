from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QWidget


class LoadFileWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.setLayout(QHBoxLayout())
		self.layout().addWidget(QLabel("File Path:"))
		self.layout().addWidget(QLineEdit())
		self.file_dialog_button = QPushButton()
		self.layout().addWidget(self.file_dialog_button)