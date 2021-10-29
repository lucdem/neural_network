from PyQt5.QtWidgets import (QComboBox, QGridLayout, QGroupBox,
	QHBoxLayout, QLabel, QSizePolicy, QSpinBox)
from PyQt5.QtCore import Qt


class TrainingParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()
		self.net_manager = net_manager

		self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)

		self.setTitle("Training Parameters")

		grid_layout = QGridLayout()
		grid_layout.addWidget(QLabel('Learning rate'), 0, 0, Qt.AlignmentFlag.AlignCenter)
		learning_rate_input = QSpinBox()
		learning_rate_input.setRange(1, 9)

		learning_rate_hbox = QHBoxLayout()
		learning_rate_hbox.addWidget(learning_rate_input)
		learning_rate_magnitude_input = QComboBox()
		learning_rate_magnitude_input.addItems([
			"10\N{SUPERSCRIPT ONE}",
			"10\N{SUPERSCRIPT ZERO}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT TWO}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT THREE}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FOUR}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT FIVE}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SIX}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SEVEN}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT EIGHT}",
			"10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT NINE}",
		])
		learning_rate_hbox.addWidget(learning_rate_magnitude_input)
		grid_layout.addLayout(learning_rate_hbox, 0, 1)

		grid_layout.addWidget(QLabel('Batch size'), 0, 2, Qt.AlignmentFlag.AlignCenter)
		batch_size_input = QSpinBox()
		batch_size_input.setRange(1, 100000)
		grid_layout.addWidget(batch_size_input, 0, 3)

		grid_layout.addWidget(QLabel('Max Epochs'), 0, 4, Qt.AlignmentFlag.AlignCenter)
		batch_size_input = QSpinBox()
		batch_size_input.setRange(1, 100000)
		grid_layout.addWidget(batch_size_input, 0, 5)

		self.setLayout(grid_layout)
