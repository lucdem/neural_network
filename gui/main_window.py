from gui.text_output_widget import TextOutputWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMenu, QSizePolicy

from .data_set_box import DataSetBox
from .graph_wrapper import GraphWrapper
from .net_params_box import NetParamsBox
from .training_params_box import TrainingParamsBox
from .layer_params_box import LayerParamsBox
from .net_list_widget import NetListWidget


class MainWindow(QWidget):
	def __init__(self, net_manager):
		super().__init__()

		self.net_manager = net_manager
		self.graph_wrapper = GraphWrapper()

		# build window
		self.top_layer_layout = QHBoxLayout()
		self.net_list_widget = NetListWidget(net_manager)
		self.center_widget = QWidget()
		self.center_widget.setLayout(QVBoxLayout())
		self.graph_widget = self.graph_wrapper.widget

		self.setWindowTitle("Neural Network")
		self.setLayout(self.top_layer_layout)

		self.top_layer_layout.addWidget(self.net_list_widget, stretch=1)
		self.top_layer_layout.addWidget(self.center_widget, stretch=3)
		self.top_layer_layout.addWidget(self.graph_widget, stretch=3)

		self.net_params_box = NetParamsBox(net_manager)
		self.center_widget.layout().addWidget(self.net_params_box, stretch=1)

		self.layer_params_box = LayerParamsBox(net_manager)
		self.center_widget.layout().addWidget(self.layer_params_box, stretch=1)

		self.training_params_box = TrainingParamsBox(net_manager)
		self.center_widget.layout().addWidget(self.training_params_box, stretch=1)

		data_sets_widget = QWidget()
		data_sets_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)
		data_sets_widget.setLayout(QHBoxLayout())
		data_sets_widget.layout().setSpacing(5)
		data_sets_widget.layout().setContentsMargins(0, 0, 0, 0)
		data_sets_widget.layout().addWidget(DataSetBox("Training Set"))
		data_sets_widget.layout().addWidget(DataSetBox("Validation Set"))
		self.center_widget.layout().addWidget(data_sets_widget, stretch=1)

		self.text_output = TextOutputWidget()
		self.center_widget.layout().addWidget(self.text_output, stretch=0)

		# event/signal bindings

		self.net_params_box.hidden_layer_count_input.valueChanged.connect(self.layer_params_box.change_hidden_layer_count)

	def show(self):
		self.showMaximized()

	def contextMenuEvent(self, event):
		menu = QMenu(self)

		new_item_action = menu.addAction('AAAA')
		new_item_action.triggered.connect(self.print)

		menu.exec(event.globalPos())