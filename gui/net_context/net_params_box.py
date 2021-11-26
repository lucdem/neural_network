from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QLabel,
	QPushButton, QSpinBox, QVBoxLayout, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt

from gui.extended_line_edit import Extended_QLineEdit


class NetParamsBox(QGroupBox):
	def __init__(self):
		super().__init__()

		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

		self.setTitle("Network Parameters")
		self.setLayout(QHBoxLayout())
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(0, 0, 0, 0)

		params_grid_widget = QWidget()
		params_grid_widget.setLayout(QGridLayout())

		buttons_container_widget = QWidget()
		buttons_container_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		buttons_container_widget.setLayout(QVBoxLayout())

		self.layout().addWidget(params_grid_widget, stretch = 1)
		self.layout().addWidget(buttons_container_widget, alignment= Qt.AlignmentFlag.AlignRight, stretch = 0)

		self.build_net_button = QPushButton("Build Network")
		buttons_container_widget.layout().addWidget(self.build_net_button)

		self.start_training_button = QPushButton("Start Training")
		self.start_training_button.setEnabled(False)
		buttons_container_widget.layout().addWidget(self.start_training_button)

		self.stop_training_button = QPushButton("Stop Training")
		self.stop_training_button.setEnabled(False)
		buttons_container_widget.layout().addWidget(self.stop_training_button)

		params_grid_widget.layout().addWidget(QLabel('Net Name'), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
		self.name_input = Extended_QLineEdit()
		params_grid_widget.layout().addWidget(self.name_input, 0, 1, 1, 5)

		params_grid_widget.layout().addWidget(QLabel('Input count'), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
		self.input_count_input = QSpinBox()
		self.input_count_input.setRange(1, 2000000)
		params_grid_widget.layout().addWidget(self.input_count_input, 1, 1)

		params_grid_widget.layout().addWidget(QLabel('Output count'), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
		self.output_count_input = QSpinBox()
		self.output_count_input.setRange(1, 2000000)
		params_grid_widget.layout().addWidget(self.output_count_input, 1, 3)

		params_grid_widget.layout().addWidget(QLabel('Hidden layer count'), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
		self.hidden_layer_count_input = QSpinBox()
		self.hidden_layer_count_input.setRange(0, 2000000)
		params_grid_widget.layout().addWidget(self.hidden_layer_count_input, 1, 5)

	def _check_values(self, net):
		self.name_input.setText(net.name)
		self.input_count_input.setValue(net.input_count)
		self.output_count_input.setValue(net.output_count)
		self.hidden_layer_count_input.setValue(len(net.layers) - 1)