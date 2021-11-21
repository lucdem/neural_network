from PyQt5.QtWidgets import (QComboBox, QGridLayout, QGroupBox,
	QHBoxLayout, QLabel, QSizePolicy, QSpinBox)
from PyQt5.QtCore import Qt


class TrainingParamsBox(QGroupBox):
	def __init__(self):
		super().__init__()

		self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)

		self.setTitle("Training Parameters")

		grid_layout = QGridLayout()
		grid_layout.addWidget(QLabel('Learning rate'), 0, 0, Qt.AlignmentFlag.AlignCenter)
		self.learning_rate_input = QSpinBox()
		self.learning_rate_input.setRange(1, 99)

		learning_rate_hbox = QHBoxLayout()
		learning_rate_hbox.addWidget(self.learning_rate_input)
		self.learning_rate_magnitude_input = QComboBox()
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT ONE}", 1)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT ZERO}", 0)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}", -1)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT TWO}", -2)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT THREE}", -3)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FOUR}", -4)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FIVE}", -5)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SIX}", -6)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SEVEN}", -7)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT EIGHT}", -8)
		self.learning_rate_magnitude_input.addItem("10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT NINE}", -9)
		# self.learning_rate_magnitude_input.addItems([
		# 	"10\N{SUPERSCRIPT ONE}",
		# 	"10\N{SUPERSCRIPT ZERO}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT TWO}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT THREE}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FOUR}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FIVE}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SIX}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SEVEN}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT EIGHT}",
		# 	"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT NINE}",
		# ])
		learning_rate_hbox.addWidget(self.learning_rate_magnitude_input)
		self.learning_rate_magnitude_input.setCurrentIndex(4)
		grid_layout.addLayout(learning_rate_hbox, 0, 1)

		grid_layout.addWidget(QLabel('Batch size'), 0, 2, Qt.AlignmentFlag.AlignCenter)
		self.batch_size_input = QSpinBox()
		self.batch_size_input.setValue(50)
		self.batch_size_input.setRange(1, 100000)
		grid_layout.addWidget(self.batch_size_input, 0, 3)

		grid_layout.addWidget(QLabel('Max Epochs'), 0, 4, Qt.AlignmentFlag.AlignCenter)
		self.max_epochs_input = QSpinBox()
		self.max_epochs_input.setValue(100)
		self.max_epochs_input.setRange(1, 100000)
		grid_layout.addWidget(self.max_epochs_input, 0, 5)

		self.setLayout(grid_layout)
