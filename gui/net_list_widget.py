from __future__ import annotations

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QFileDialog
from PyQt5.QtCore import pyqtSignal

from app import NetManager


class NetListWidget(QListWidget):
	selected_net_changed_signal = pyqtSignal(int)

	def __init__(self, net_manager):
		super().__init__()
		self.net_manager: NetManager = net_manager
		self.itemSelectionChanged.connect(self.change_selected_net)

		self.new_net()

	def contextMenuEvent(self, event):
		menu = QMenu(self)

		new_net_action = menu.addAction('New net')
		new_net_action.triggered.connect(self.new_net)

		new_net_action = menu.addAction('Load net')
		new_net_action.triggered.connect(self.load_net)

		pos = event.pos()
		item = self.itemAt(pos)
		if item is not None:
			remove_net_action = menu.addAction('Remove net')
			remove_net_action.triggered.connect(lambda: self.remove_net(item))

			save_net_action = menu.addAction("Save net")
			save_net_action.triggered.connect(lambda: self.save_net(item))

		menu.exec(event.globalPos())

	def _new_item(self, net_id):
		new_item = NetListItem(self.net_manager.net_by_id[net_id].name, net_id)
		self.addItem(new_item)
		self.setCurrentItem(new_item)

	def new_net(self):
		self._new_item(self.net_manager.new_net())

	def load_net(self):
		default_filter = "JSON (*.json)"
		path = QFileDialog.getOpenFileName(self, filter = default_filter)[0]
		print(path)
		if path is None:
			return
		self._new_item(self.net_manager.load_net(path))

	def remove_net(self, item):
		self.net_manager.remove_net(item.net_id)
		self.removeItemWidget(item)

	def save_net(self, item: NetListItem):
		default_filter = "JSON (*.json)"
		path = QFileDialog.getSaveFileName(self, filter = default_filter)[0]
		if path is None:
			return
		self.net_manager.save_net(path, item.net_id)

	def change_selected_net_name(self, name):
		self.currentItem().setText(name)

	def change_selected_net(self):
		self.net_manager.change_selected_net(self.currentItem().net_id)


class NetListItem(QListWidgetItem):
	def __init__(self, name, net_id):
		super().__init__(name)
		self.net_id = net_id