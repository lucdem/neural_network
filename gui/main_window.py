from app.net_manager import NetManager
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

		self.net_manager: NetManager = net_manager
		self.graph_wrapper = GraphWrapper()

		# build window
		self.top_layer_layout = QHBoxLayout()
		self.net_list_widget = NetListWidget(net_manager)
		self.center_layout = QVBoxLayout()
		self.graph_widget = self.graph_wrapper.widget

		self.setWindowTitle("Neural Network")
		self.setLayout(self.top_layer_layout)

		self.top_layer_layout.addWidget(self.net_list_widget, stretch=1)
		self.top_layer_layout.addLayout(self.center_layout, stretch=3)
		self.top_layer_layout.addWidget(self.graph_widget, stretch=3)

		self.net_params_box = NetParamsBox(net_manager)
		self.center_layout.addWidget(self.net_params_box, stretch=1)

		self.layer_params_box = LayerParamsBox(net_manager)
		self.center_layout.addWidget(self.layer_params_box, stretch=1)

		self.training_params_box = TrainingParamsBox(net_manager)
		self.center_layout.addWidget(self.training_params_box, stretch=1)

		data_sets_layout = QHBoxLayout()
		data_sets_layout.addWidget(DataSetBox("Training Set"))
		data_sets_layout.addWidget(DataSetBox("Validation Set"))
		self.center_layout.addLayout(data_sets_layout, stretch=1)

		self.text_output = TextOutputWidget()
		self.center_layout.addWidget(self.text_output, stretch=0)

		# event/signal bindings

		self.net_params_box.input_count_input.valueChanged.connect(self.layer_params_box.set_input_layer_size)
		self.net_params_box.output_count_input.valueChanged.connect(self.layer_params_box.set_output_layer_size)
		self.net_params_box.hidden_layer_count_input.valueChanged.connect(self.layer_params_box.change_hidden_layer_count)

		self.net_params_box.build_net_button.clicked.connect(self.build_net)
		self.net_params_box.name_input.edit_finished_value_signal.connect(self.net_list_widget.change_selected_net_name)

	def show(self):
		self.showMaximized()

	def contextMenuEvent(self, event):
		menu = QMenu(self)

		new_item_action = menu.addAction('AAAA')
		new_item_action.triggered.connect(self.print)

		menu.exec(event.globalPos())

	def build_net(self):
		name = self.net_params_box.name_input.text()
		input_count = self.net_params_box.input_count_input.value()
		layer_sizes = self.layer_params_box.get_layer_sizes()
		neuron_type = self.layer_params_box.default_layer_type_input.selected_type()
		self.net_manager.build_net(name, neuron_type, input_count, layer_sizes)