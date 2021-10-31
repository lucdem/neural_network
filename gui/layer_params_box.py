from typing import List

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSizePolicy, QSpinBox, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt

from .layer_type_combo_box import LayerTypeComboBox
from app import NeuronTypeEnum


class LayerParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()
		self.net_manager = net_manager

		self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)

		self.setTitle("Layer Parameters")
		self.setLayout(QVBoxLayout())

		defaults_widget = QWidget()
		defaults_widget.setLayout(QHBoxLayout())
		defaults_widget.layout().addWidget(QLabel("Default hidden layer type"))
		self.default_layer_type_input = LayerTypeComboBox()
		defaults_widget.layout().addWidget(self.default_layer_type_input)
		defaults_widget.layout().addStretch()
		self.layout().addWidget(defaults_widget)

		self.scroll_area = QScrollArea()
		self.scroll_area.verticalScrollBar().setEnabled(False)
		self.scroll_area.verticalScrollBar().setVisible(False)
		scroll_area_contents = QWidget()
		self.scroll_area_layout = QHBoxLayout(scroll_area_contents)
		self.scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.scroll_area.setWidget(scroll_area_contents)
		self.scroll_area.setWidgetResizable(True)
		self.layout().addWidget(self.scroll_area)

		self.input_layer_box = InputLayerInnerBox()
		self.output_layer_box = OutputLayerInnerBox()

		self.append_layer(self.input_layer_box)
		self.append_layer(self.output_layer_box)

	def append_layer(self, inner_box):
		self.scroll_area_layout.addWidget(inner_box)

	def insert_layer(self, inner_box, index):
		self.scroll_area_layout.insertWidget(index, inner_box)

	def remove_layer(self):
		self.scroll_area_layout.removeWidget(self.scroll_area_layout.itemAt(self.scroll_area_layout.count() - 2).widget())

	def set_input_layer_size(self, size):
		self.input_layer_box.size_input.setValue(size)

	def set_output_layer_size(self, size):
		self.output_layer_box.size_input.setValue(size)

	def change_hidden_layer_count(self, count):
		if count > self.scroll_area_layout.count() - 2:
			self.insert_layer(HiddenLayerInnerBox(
				self.default_layer_type_input.itemData(self.default_layer_type_input.currentIndex())), count)
		elif count < self.scroll_area_layout.count() - 2:
			self.remove_layer()


class LayerInnerBox(QGroupBox):
	def __init__(self, label):
		super().__init__()

		self.setLayout(QVBoxLayout())
		self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setTitle(label)

		self.layout().addWidget(QLabel("Layer Size"))
		self.size_input = QSpinBox()
		self.size_input.setValue(1)
		self.size_input.setRange(1, 1000000)
		self.layout().addWidget(self.size_input)

	def change_size(self, size):
		self.size_input = size


class InputLayerInnerBox(LayerInnerBox):
	def __init__(self):
		super().__init__("Input Layer")
		self.size_input.setDisabled(True)


class OutputLayerInnerBox(LayerInnerBox):
	def __init__(self):
		super().__init__("Output Layer")
		self.size_input.setDisabled(True)

		self.layout().addWidget(QLabel("Layer Type"))
		self.type_input = LayerTypeComboBox()
		self.layout().addWidget(self.type_input)


class HiddenLayerInnerBox(LayerInnerBox):
	def __init__(self, initial_type: NeuronTypeEnum = None):
		super().__init__("Hidden Layer")

		self.layout().addWidget(QLabel("Layer Type"))
		self.type_input = LayerTypeComboBox(initial_type)
		self.layout().addWidget(self.type_input)