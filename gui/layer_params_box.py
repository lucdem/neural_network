from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea, QWidget


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

		test = Test("test test")

		for i in range(30):
			self.add_layer(test, i)

	def add_layer(self, layer, n):
		inner_box = QGroupBox()
		self.scroll_area_layout.addWidget(inner_box)
		inner_box.setLayout(QVBoxLayout())
		inner_box.setTitle(f"Layer {n}")

		label = QLabel(layer.type_name)
		inner_box.layout().addWidget(label)


class Test:
	def __init__(self, name):
		self.type_name = name