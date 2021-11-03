from app.net_manager import NetManager
from gui.text_output_widget import TextOutputWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMenu, QSizePolicy

from .data_set_box import DataSetBox
from .graph_wrapper import GraphWrapper
from .net_params_box import NetParamsBox
from .training_params_box import TrainingParamsBox
from .layer_params_box import LayerParamsBox
from .net_list_widget import NetListWidget
from .net_stacked_layout import NetStackedLayout
from gui import net_stacked_layout


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

		self.net_stacked_layout = NetStackedLayout(self.net_manager)
		self.center_layout.addLayout(self.net_stacked_layout)

		self.text_output = TextOutputWidget()
		self.center_layout.addWidget(self.text_output, stretch=0)

		# event/signal bindings

		self.net_list_widget.selected_net_changed_signal.connect(self.net_manager.change_selected_net)
		self.net_manager.update_name_listeners.append(self.net_list_widget.change_selected_net_name)

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