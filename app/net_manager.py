from typing import Iterable, List, Callable, Dict, Tuple
import os
import json


from neural_network import LinearNeuron, JsonlDataStream, MeanSquareError
from .extended_neural_network import ExtendedNeuralNetwork, NetJsonEnconder, NetJsonDecoder
from .data_classes.training_params import TrainingParams


class NetManager:
	def __init__(self):
		self.net_by_id: Dict[int, ExtendedNeuralNetwork] = {}
		self.selected_net_id = -1
		self.last_assigned_id = -1
		self.selection_change_listeners: List[Callable] = []
		self.update_name_listeners: List[Callable] = []

	@property
	def selected_net(self) -> ExtendedNeuralNetwork:
		return self.net_by_id[self.selected_net_id]

	def _new_net(self, net) -> int:
		self.last_assigned_id += 1
		last_id = self.last_assigned_id
		self.net_by_id[last_id] = net
		self.change_selected_net(last_id)
		return last_id

	def new_net(self) -> int:
		net = ExtendedNeuralNetwork(LinearNeuron, 1, [1])
		return self._new_net(net)

	def load_net(self, path) -> int:
		with open(path, mode = 'r') as f:
			net = json.loads(f.read(), cls = NetJsonDecoder)
		return self._new_net(net)

	def build_net(self, neuron_type, input_count, layer_sizes, name):
		self.net_by_id[self.last_assigned_id] = ExtendedNeuralNetwork(neuron_type, input_count, layer_sizes, name)

	def train_net(self, net_id, params: TrainingParams,
		cost_function = MeanSquareError) -> Iterable[Tuple[int, float, float]]:

		training_data = JsonlDataStream(params.training_data_path)
		validation_data = JsonlDataStream(params.validation_data_path)
		for epoch in range(params.max_epochs):
			self.net_by_id[net_id].train(1, params.learning_rate, params.batch_size, training_data, cost_function)
			cost, acc = self.net_by_id[net_id].validate(validation_data, cost_function)
			yield epoch, cost, acc

	# def remove_net(self, id):
	# 	self.net_by_id.pop(id)
	# 	for listener in self.net_removal_listeners:
	# 		listener()

	def change_selected_net(self, selected_id):
		if selected_id == self.selected_net_id:
			return
		self.selected_net_id = selected_id
		for listener in self.selection_change_listeners:
			listener()

	def update_net_name(self, name):
		self.selected_net.name = name
		for listener in self.update_name_listeners:
			listener(self.selected_net.name)

	def save_net(self, path, net_id):
		split_path = os.path.splitext(path)
		if split_path[1] != ".json":
			path = "".join((split_path[0], ".json"))
		with open(path, mode='w') as f:
			f.write(json.dumps(self.net_by_id[net_id], cls = NetJsonEnconder))
