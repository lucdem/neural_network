from typing import List, Callable, Dict

from neural_network import LinearNeuron
from .extended_neural_network import ExtendedNeuralNetwork


class NetManager():
	def __init__(self):
		self.net_by_id: Dict[int, ExtendedNeuralNetwork] = {}
		self.selected_net_id = -1
		self.last_assigned_id = -1
		self.selection_change_listeners: List[Callable] = []
		# self.update_listeners: List[Callable] = []
		# self.net_removal_listeners: List[Callable] = []

	@property
	def selected_net(self) -> ExtendedNeuralNetwork:
		return self.net_by_id[self.selected_net_id]

	def new_net(self):
		net = ExtendedNeuralNetwork("New net", LinearNeuron, 0, [0])
		self.last_assigned_id += 1
		id = self.last_assigned_id
		self.net_by_id[id] = net
		self.change_selected_net(id)

	def remove_net(self, id):
		self.net_by_id.pop(id)
		# for listener in self.net_removal_listeners:
		# 	listener()

	def change_selected_net(self, selected_id):
		if selected_id == self.selected_net_id:
			return
		self.selected_net_id = selected_id
		for listener in self.selection_change_listeners:
			listener()

	def update_net(self):
		for listener in self.update_listeners:
			listener()