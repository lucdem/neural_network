from typing import List

from neural_network import NeuralNetwork, LinearNeuron


class NetManager():
	def __init__(self):
		self.net_by_id = {}
		self.selected_net_id = -1
		self.last_assigned_id = -1
		pass

	def new_net(self) -> int:
		net = NeuralNetwork(LinearNeuron, 0, [0])
		self.last_assigned_id += 1
		id = self.last_assigned_id
		self.net_by_id[id] = net
		return id

	def remove_net(self, id):
		self.neural_nets.pop(id)
