from typing import Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStackedLayout

from app import NetManager
from .net_context.net_context_widget import NetContextWidget


class NetStackedLayout(QStackedLayout):
	net_name_changed_signal = pyqtSignal(int, str)
	net_built_signal = pyqtSignal(int)

	training_started_signal = pyqtSignal(int, int)
	training_progress_signal = pyqtSignal(int, int, float, float)
	training_finished_signal = pyqtSignal(int)

	def __init__(self, net_manager: NetManager) -> None:
		super().__init__()
		self.net_manager = net_manager
		self.context_widget_by_id: Dict[int, NetContextWidget] = {}
		self.__add_new_context()

	def __add_new_context(self) -> int:
		new_context = NetContextWidget(self.net_manager)
		new_context.net_params_box.name_input.edit_finished_value_signal.connect(
			lambda name: self.net_name_changed_signal.emit(self.net_manager.selected_net_id, name)
		)
		new_context.net_built_signal.connect(self.net_built_signal.emit)
		new_context.training_worker.started.connect(self.training_started_signal.emit)
		new_context.training_worker.progress.connect(self.training_progress_signal.emit)
		new_context.training_worker.finished.connect(self.training_finished_signal.emit)
		self.context_widget_by_id[self.net_manager.selected_net_id] = new_context
		index = self.addWidget(new_context)
		return index

	def change_context(self):
		context = self.context_widget_by_id.get(self.net_manager.selected_net_id)
		if context is None:
			index = self.__add_new_context()
		else:
			index = self.indexOf(context)
		self.setCurrentIndex(index)

	def remove_context(self, net_id):
		self.removeWidget(self.context_widget_by_id[net_id])
		self.context_widget_by_id.pop(net_id)