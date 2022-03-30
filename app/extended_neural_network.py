from typing import Dict, Type, List
from json import JSONEncoder, JSONDecoder

import numpy as np

from neural_network import NeuralNetwork, ActivationFunction, Layer
from .activation_function_enum import ActivationFunctionEnum


class ExtendedNeuralNetwork(NeuralNetwork):
	def __init__(self, neuron_type: Type[ActivationFunction], input_count, layer_sizes: List[int], name = "New net"):
		super().__init__(neuron_type, input_count, layer_sizes)
		self.name: str = name

	def __getstate__(self):
		return {
			'name': self.name,
			'input_count': self.input_count,
			'layers': [{
				'neuron_type': ActivationFunctionEnum(type(layer.neurons[0])).name,
				'weight_matrix': [neuron.weights for neuron in layer.neurons]
			} for layer in self.layers]
		}

	def __setstate__(self, state):
		layers = []
		for layer_state in state['layers']:
			neurons = []
			for weights in range(layer_state['weight_matrix'].shape[1]):
				neuron = ActivationFunctionEnum[layer_state['neuron_type']].value(weights.size)
				neuron.weights = weights
			layers.append(Layer.create_from_neurons(neurons))

		self.layers = layers


class NetJsonEnconder(JSONEncoder):
	def default(self, obj: ExtendedNeuralNetwork):
		if isinstance(obj, ExtendedNeuralNetwork):
			return obj.__dict__
		elif isinstance(obj, Layer):
			return {
				'activation_function': obj.activation_function.__name__,
				'weight_matrix': obj.weight_matrix,
				'biases': obj.biases
			}
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		return super().default(obj)


class NetJsonDecoder(JSONDecoder):
	def __init__(self) -> None:
		super().__init__(object_hook = self._net_decode)

	def _net_decode(self, dict: Dict):
		weights = dict.get('weight_matrix')
		if weights is None:
			net = ExtendedNeuralNetwork.create_from_layers(dict['layers'])
			net.name = dict['name']
			return net
		else:
			weights = np.array(weights)
			layer = Layer(ActivationFunctionEnum[dict['activation_function']].value, weights.shape[1], weights.shape[0])
			layer.weight_matrix = weights
			layer.biases = np.array(dict['biases'])
			return layer