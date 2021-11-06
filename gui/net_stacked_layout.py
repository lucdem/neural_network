from PyQt5.QtWidgets import QStackedLayout

from app import NetManager
from .net_context_widget import NetContextWidget


class NetStackedLayout(QStackedLayout):
	def __init__(self, net_manager: NetManager) -> None:
		super().__init__()
		self.net_manager = net_manager

		self.index_by_id = {}
		self.index_by_id[self.net_manager.selected_net_id] = 0

		self.addWidget(NetContextWidget(net_manager))
		self.net_manager.selection_change_listeners.append(self.switch_context)

	def switch_context(self):
		index = self.index_by_id.get(self.net_manager.selected_net_id)
		if index is None:
			index = self.addWidget(NetContextWidget(self.net_manager))
			self.index_by_id[self.net_manager.selected_net_id] = index
		self.setCurrentIndex(index)