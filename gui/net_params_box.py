from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QLabel,
	QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt

from app import NetManager


class NetParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()

		self.net_manager: NetManager = net_manager

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
		self.build_net_button.clicked.connect(self.build_net)
		buttons_container_widget.layout().addWidget(self.build_net_button)

		self.train_net_button = QPushButton("Start Training")
		self.train_net_button.clicked.connect(self.train_net)
		buttons_container_widget.layout().addWidget(self.train_net_button)

		self.train_net_button = QPushButton("Pause Training")
		self.train_net_button.clicked.connect(self.train_net)
		buttons_container_widget.layout().addWidget(self.train_net_button)

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
		self.hidden_layer_count_input.setRange(0, 2000000)
		params_grid_widget.layout().addWidget(self.hidden_layer_count_input, 1, 5)

	def build_net(self):
		return
		# self.net_manager.build_net(self.name_input.text,
		# 	self.input_count_input.value(), self.input_count_input.value(), )

	def train_net(self):
		return
		# self.net_manager.build_net(self.name_input.text,
		# 	self.input_count_input.value(), self.input_count_input.value(), )