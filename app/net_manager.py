from typing import Iterable, List, Callable, Dict, Tuple
import os
import json


from neural_network import Layer, SigmoidLogisticNeuron, JsonlDataStream, MeanSquareError
from .extended_neural_network import ExtendedNeuralNetwork, NetJsonEnconder, NetJsonDecoder
from .data_classes.training_params import TrainingParams
from app.neuron_type_enum import NeuronTypeEnum


class NetManager:
	def __init__(self):
		self.net_by_id: Dict[int, ExtendedNeuralNetwork] = {}
		self.selected_net_id = -1
		self.last_assigned_id = -1

	@property
	def selected_net(self) -> ExtendedNeuralNetwork:
		return self.net_by_id[self.selected_net_id]

	def _new_net(self, net) -> int:
		self.last_assigned_id += 1
		last_id = self.last_assigned_id
		self.net_by_id[last_id] = net
		return last_id

	def new_net(self) -> int:
		net = ExtendedNeuralNetwork(SigmoidLogisticNeuron, 1, [1])
		return self._new_net(net)

	def change_selected_net(self, selected_id: int):
		self.selected_net_id = selected_id

	def load_net(self, path: str) -> int:
		with open(path, mode = 'r') as f:
			net = json.loads(f.read(), cls = NetJsonDecoder)
		return self._new_net(net)

	def build_net(self, net_id: int, input_count: int, layer_sizes: List[int], layer_types: List[NeuronTypeEnum]):
		name = self.net_by_id[net_id].name
		layers = [Layer(layer_types[0].value, input_count, layer_sizes[0])]
		for i in range(1, len(layer_sizes)):
			layers.append(Layer(layer_types[i].value, layer_sizes[i - 1], layer_sizes[i]))
		net_built = ExtendedNeuralNetwork.create_from_layers(layers)
		net_built.name = name
		self.net_by_id[net_id] = net_built

	def train_net(self, net_id: int, training_data_path: str, validation_data_path: str,
		params: TrainingParams) -> Iterable[Tuple[int, float, float]]:

		training_data = JsonlDataStream(training_data_path)
		validation_data = JsonlDataStream(validation_data_path)
		for epoch in range(params.max_epochs):
			self.net_by_id[net_id].train(1, params.learning_rate, params.friction,
				params.batch_size, params.dropout, training_data, params.cost_function)
			cost, acc = self.net_by_id[net_id].validate(validation_data, params.cost_function)
			yield epoch, cost, acc

	def remove_net(self, id: int):
		self.net_by_id.pop(id)

	def save_net(self, path: str, net_id: int):
		split_path = os.path.splitext(path)
		if split_path[1] != ".json":
			path = "".join((split_path[0], ".json"))
		with open(path, mode='w') as f:
			net_json = json.dumps(self.net_by_id[net_id], cls = NetJsonEnconder, indent='\t')
			f.write(net_json)
