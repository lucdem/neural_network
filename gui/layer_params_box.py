from typing import List

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QScrollArea, QWidget


class LayerParamsBox(QGroupBox):
	def __init__(self, net_manager):
		super().__init__()
		self.net_manager = net_manager

		self.setTitle("Layer Parameters")
		self.setLayout(QHBoxLayout())
		self.scroll_area = QScrollArea()
		self.scroll_area.verticalScrollBar().setEnabled(False)
		self.scroll_area.verticalScrollBar().setVisible(False)
		scroll_area_contents = QWidget()
		self.scroll_area_layout = QHBoxLayout(scroll_area_contents)
		self.scroll_area.setWidget(scroll_area_contents)
		self.scroll_area.setWidgetResizable(True)
		self.layout().addWidget(self.scroll_area)

		self.append_layer("Input Layer")
		self.append_layer("Hidden Layer")
		self.append_layer("Output Layer")

	def append_layer(self, label):
		inner_box = InnerBox(label)
		self.scroll_area_layout.addWidget(inner_box)

	def insert_layer(self, label, index):
		inner_box = InnerBox(label)
		self.scroll_area_layout.insertWidget(index, inner_box)

	def remove_layer(self):
		self.scroll_area_layout.removeWidget(self.scroll_area_layout.itemAt(self.scroll_area_layout.count() - 2).widget())

	def change_hidden_layer_count(self, count):
		if count > self.scroll_area_layout.count() - 2:
			self.insert_layer("Hidden Layer", count)
		elif count < self.scroll_area_layout.count() - 2:
			self.remove_layer()


class InnerBox(QGroupBox):
	def __init__(self, label):
		super().__init__()

		self.setLayout(QVBoxLayout())
		self.setTitle(label)

		self.layout().addWidget(QLabel("Layer Size"))
		self.size_input = QSpinBox()
		self.layout().addWidget(self.size_input)