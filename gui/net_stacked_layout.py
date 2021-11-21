from typing import Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStackedLayout

from app import NetManager
from .net_context.net_context_widget import NetContextWidget


class NetStackedLayout(QStackedLayout):
	training_started = pyqtSignal(int, int)
	training_progress = pyqtSignal(int, int, float, float)
	training_finished = pyqtSignal(int)

	def __init__(self, net_manager: NetManager) -> None:
		super().__init__()
		self.net_manager = net_manager
		self.index_by_id: Dict[int, int] = {}

		self.__add_new_context()
		self.net_manager.selection_change_listeners.append(self.switch_context)

	def __add_new_context(self) -> int:
		new_context = NetContextWidget(self.net_manager)
		new_context.training_worker.started.connect(self.__training_start_handler)
		new_context.training_worker.progress.connect(self.__training_progress_handler)
		new_context.training_worker.finished.connect(self.__training_finished_handler)
		index = self.addWidget(new_context)
		self.index_by_id[self.net_manager.selected_net_id] = index
		return index

	def __training_start_handler(self, net_id, max_epochs):
		self.training_started.emit(net_id, max_epochs)

	def __training_progress_handler(self, net_id, epoch, cost, acc):
		self.training_progress.emit(net_id, epoch, cost, acc)

	def __training_finished_handler(self, net_id):
		self.training_finished.emit(net_id)

	def switch_context(self):
		index = self.index_by_id.get(self.net_manager.selected_net_id)
		if index is None:
			index = self.__add_new_context()
		self.setCurrentIndex(index)