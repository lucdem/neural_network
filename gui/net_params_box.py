from PyQt5.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QWidget
from PyQt5.QtCore import Qt

from .layer_params_box import LayerParamsBox

from app import NetManager


class NetParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()

		self.net_manager: NetManager = net_manager

		self.setTitle("Network Parameters")
		self.setLayout(QHBoxLayout())

		params_grid_widget = QWidget()
		params_grid_widget.setLayout(QGridLayout())

		self.layout().addWidget(params_grid_widget)
		self.build_net_button = QPushButton("Build\nNetwork")
		self.build_net_button.setFixedWidth(self.build_net_button.fontMetrics().width(self.build_net_button.text()) + 15)
		self.build_net_button.setFixedHeight(self.build_net_button.width())
		self.layout().addWidget(self.build_net_button)
		self.build_net_button.clicked.connect(self.build_net)

		params_grid_widget.layout().addWidget(QLabel('Net Name'), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
		self.name_input = QLineEdit()
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
		self.hidden_layer_count_input.setRange(1, 2000000)
		params_grid_widget.layout().addWidget(self.hidden_layer_count_input, 1, 5)

	def build_net(self):
		self.net_manager.build_net(self.name_input.text, self.input_count_input.value(), self.input_count_input.value(), )