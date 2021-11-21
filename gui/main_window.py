from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMenu

from app.net_manager import NetManager

from .text_output_widget import TextOutputWidget
from .plotting.graphics_wrapper import GraphicsWrapper
from .net_list_widget import NetListWidget
from .net_stacked_layout import NetStackedLayout

from random import uniform


class MainWindow(QWidget):
	def __init__(self, net_manager):
		super().__init__()

		self.net_manager: NetManager = net_manager
		self.graph_wrapper = GraphicsWrapper(net_manager)

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

		self.net_manager.update_name_listeners.append(self.net_list_widget.change_selected_net_name)
		self.net_stacked_layout.training_started.connect(self.graph_wrapper.create_plot_data)
		self.net_stacked_layout.training_progress.connect(self.graph_wrapper.update_graphs)
		self.net_stacked_layout.training_progress.connect(self.print_training_progress_msg)

		self.coisacoisacoisa = 0

	def show(self):
		self.showMaximized()

	def contextMenuEvent(self, event):
		menu = QMenu(self)

		test = menu.addAction('test')
		test.triggered.connect(self.test)

		menu.exec(event.globalPos())

	def test(self):
		self.coisacoisacoisa += 1
		self.net_manager.emit_training_progression(self.coisacoisacoisa, 100, uniform(0, 10000), uniform(0, 100))

	def print_training_progress_msg(self, net_id, epoch, cost, acc):
		self.text_output.message('training...', net_name = self.net_manager.net_by_id[net_id].name,
			epoch = epoch, cost = cost, acc = acc)