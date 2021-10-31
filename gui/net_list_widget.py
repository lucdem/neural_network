from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu

from app import NetManager


class NetListWidget(QListWidget):
	def __init__(self, net_manager):
		super().__init__()
		self.net_manager: NetManager = net_manager

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

		menu.exec(event.globalPos())

	def new_net(self):
		self.net_manager.new_net()
		self.addItem(NetListItem(self.net_manager.selected_net.name, self.net_manager.selected_net_id))

	def remove_net(self, item):
		self.net_manager.remove_net(item.net_id)
		self.removeItemWidget(item)

	def change_selected_net_name(self, name):
		self.currentItem().setText(name)
		pass


class NetListItem(QListWidgetItem):
	def __init__(self, name, net_id):
		super().__init__(name)
		self.net_id = net_id