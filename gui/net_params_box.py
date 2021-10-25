from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt


class NetParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()

		self.setTitle("Network Parameters")
		self.setLayout(QGridLayout())

		self.layout().addWidget(QLabel('Net Name'), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
		self.name_input = QLineEdit()
		self.layout().addWidget(self.name_input, 0, 1, 1, 5)

		self.layout().addWidget(QLabel('Input count'), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
		self.input_count_input = QSpinBox()
		self.input_count_input.setRange(1, 2000000)
		self.layout().addWidget(self.input_count_input, 1, 1)

		self.layout().addWidget(QLabel('Output count'), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
		self.output_count_input = QSpinBox()
		self.output_count_input.setRange(1, 2000000)
		self.layout().addWidget(self.output_count_input, 1, 3)

		self.layout().addWidget(QLabel('Hidden layer count'), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
		self.hidden_layer_count_input = QSpinBox()
		self.hidden_layer_count_input.setRange(1, 2000000)
		self.layout().addWidget(self.hidden_layer_count_input, 1, 5)

		# self.addWidget(QLabel('Input count'), 1, 0)
		# input_count_input = QSpinBox()
		# self.addWidget(input_count_input, 1, 1)

		# self.addWidget(QLabel('Output count'), 1, 3)
		# output_count_input = QSpinBox()
		# self.addWidget(output_count_input, 1, 4)

		# self.addWidget(QLabel('Hidden layer count'), 1, 6)
		# layer_count_input = QSpinBox()
		# self.addWidget(layer_count_input, 1, 7)