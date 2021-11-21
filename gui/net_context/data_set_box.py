from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSizePolicy, QLineEdit, QPushButton, QLabel, QFileDialog


class DataSetBox(QGroupBox):
	def __init__(self, title):
		super().__init__()

		self.setTitle(title)

		self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)

		self.setLayout(QHBoxLayout())
		self.layout().addWidget(QLabel("File Path:"))
		self.file_path_input = QLineEdit()
		self.layout().addWidget(self.file_path_input)
		self.file_dialog_button = QPushButton("Select\nfile")
		self.file_dialog_button.clicked.connect(self.file_dialog)
		self.file_dialog_button.setFixedWidth(self.file_dialog_button.fontMetrics().width(self.file_dialog_button.text()))
		self.file_dialog_button.setFixedHeight(self.file_dialog_button.width())
		self.layout().addWidget(self.file_dialog_button)

	def file_dialog(self):
		self.file_path_input.setText(QFileDialog.getOpenFileName(self, filter="JSON lines (*.jsonl)")[0])