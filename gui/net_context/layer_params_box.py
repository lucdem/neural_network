from __future__ import annotations
from typing import List

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSizePolicy, QSpinBox, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt

from .layer_type_combo_box import LayerTypeComboBox
from app import ActivationFunctionEnum


class LayerParamsBox(QGroupBox):
	def __init__(self):
		super().__init__()

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

		self.hidden_layers_inner_boxes: List[HiddenLayerInnerBox] = []

		self.input_layer_box = InputLayerInnerBox()
		self.output_layer_box = OutputLayerInnerBox()

		self.__append_layer(self.input_layer_box)
		self.__append_layer(self.output_layer_box)

	def __append_layer(self, inner_box):
		self.scroll_area_layout.addWidget(inner_box)

	def add_hidden_layer(self, inner_box):
		self.hidden_layers_inner_boxes.append(inner_box)
		self.scroll_area_layout.insertWidget(self.scroll_area_layout.count() - 1, inner_box)

	def remove_layer(self):
		self.hidden_layers_inner_boxes.pop()
		self.scroll_area_layout.removeWidget(self.scroll_area_layout.itemAt(self.scroll_area_layout.count() - 2).widget())

	def set_input_layer_size(self, size):
		self.input_layer_box.size_input.setValue(size)

	def set_output_layer_size(self, size):
		self.output_layer_box.size_input.setValue(size)

	def change_hidden_layer_count(self, count):
		while count > self.scroll_area_layout.count() - 2:
			self.add_hidden_layer(HiddenLayerInnerBox(
				self.default_layer_type_input.itemData(self.default_layer_type_input.currentIndex())))
		else:
			while count < self.scroll_area_layout.count() - 2:
				self.remove_layer()

	def get_layer_sizes(self):
		sizes = [inner_box.size_input.value() for inner_box in self.hidden_layers_inner_boxes]
		sizes.append(self.output_layer_box.size_input.value())
		return sizes

	def get_layer_types(self) -> List[ActivationFunctionEnum]:
		types = [inner_box.type_input.get_selected_type() for inner_box in self.hidden_layers_inner_boxes]
		types.append(self.output_layer_box.type_input.get_selected_type())
		return types

	def _check_values(self, layers):
		for i, layer_box in enumerate(self.hidden_layers_inner_boxes):
			layer_box.size_input.setValue(layers[i].size)
			layer_box.type_input.set_selected_type(ActivationFunctionEnum(layers[i].activation_function))

		self.output_layer_box.size_input.setValue(layers[-1].size)
		self.output_layer_box.type_input.set_selected_type(ActivationFunctionEnum(layers[-1].activation_function))


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
	def __init__(self, initial_type: ActivationFunctionEnum = None):
		super().__init__("Hidden Layer")

		self.layout().addWidget(QLabel("Layer Type"))
		self.type_input = LayerTypeComboBox(initial_type)
		self.layout().addWidget(self.type_input)