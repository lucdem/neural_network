from __future__ import annotations
import os
import json

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QFileDialog
from PyQt5.QtCore import pyqtSignal

from app import NetManager, NetJsonEnconder


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

		pos = event.pos()
		item = self.itemAt(pos)
		if item is not None:
			remove_net_action = menu.addAction('Remove net')
			remove_net_action.triggered.connect(lambda: self.remove_net(item))

			save_net_action = menu.addAction("Save net")
			save_net_action.triggered.connect(lambda: self.save_net(item))

		menu.exec(event.globalPos())

	def new_net(self):
		self.net_manager.new_net()
		new_item = NetListItem(self.net_manager.selected_net.name, self.net_manager.selected_net_id)
		self.addItem(new_item)
		self.setCurrentItem(new_item)

	def remove_net(self, item):
		self.net_manager.remove_net(item.net_id)
		self.removeItemWidget(item)

	def save_net(self, item: NetListItem):
		default_filter = "JSON (.json)"
		path = QFileDialog.getSaveFileName(self, filter = default_filter, initialFilter = default_filter)[0]
		if path is None:
			return
		split_path = os.path.splitext(path)
		if split_path[1] != ".json":
			path = "".join((split_path[0], ".json"))
		with open(path, mode='w') as f:
			f.write(json.dumps(self.net_manager.net_by_id[item.net_id], cls = NetJsonEnconder))

	def change_selected_net_name(self, name):
		self.currentItem().setText(name)

	def change_selected_net(self):
		self.net_manager.change_selected_net(self.currentItem().net_id)


class NetListItem(QListWidgetItem):
	def __init__(self, name, net_id):
		super().__init__(name)
		self.net_id = net_id