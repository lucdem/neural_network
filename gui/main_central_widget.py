from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from app.net_manager import NetManager

from .text_output_widget import TextOutputWidget
from .plotting.graphics_wrapper import GraphicsWrapper
from .net_list_widget import NetListWidget
from .net_stacked_layout import NetStackedLayout


class MainCentralWidget(QWidget):
	def __init__(self, net_manager: NetManager):
		super().__init__()

		self.net_manager: NetManager = net_manager
		self.graph_wrapper = GraphicsWrapper(net_manager)

		# build window
		self.top_layer_layout = QHBoxLayout()
		self.net_list_widget = NetListWidget(net_manager)
		self.center_layout = QVBoxLayout()
		self.graph_widget = self.graph_wrapper.widget

		self.setLayout(self.top_layer_layout)

		self.top_layer_layout.addWidget(self.net_list_widget, stretch=1)
		self.top_layer_layout.addLayout(self.center_layout, stretch=3)
		self.top_layer_layout.addWidget(self.graph_widget, stretch=3)

		self.net_stacked_layout = NetStackedLayout(self.net_manager)
		self.center_layout.addLayout(self.net_stacked_layout)

		self.text_output = TextOutputWidget(net_manager)
		self.center_layout.addWidget(self.text_output, stretch=0)

		# event/signal bindings

		self.net_stacked_layout.net_name_changed_signal.connect(self.net_list_widget.change_selected_net_name)
		self.net_stacked_layout.net_name_changed_signal.connect(self.text_output.net_name_change_msg)
		self.net_stacked_layout.net_built_signal.connect(self.text_output.net_built_msg)

		self.net_list_widget.removed_net_signal.connect(self.net_stacked_layout.remove_context)
		self.net_list_widget.selected_net_changed_signal.connect(self.net_stacked_layout.change_context)

		self.net_stacked_layout.training_started_signal.connect(self.graph_wrapper.create_plot_data)
		self.net_stacked_layout.training_started_signal.connect(self.text_output.training_started_msg)
		self.net_stacked_layout.training_progress_signal.connect(self.graph_wrapper.update_graphs)
		self.net_stacked_layout.training_progress_signal.connect(self.text_output.training_progress_msg)