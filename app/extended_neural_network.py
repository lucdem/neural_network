from typing import Dict, Type, List
from json import JSONEncoder, JSONDecoder

import numpy

from neural_network import NeuralNetwork, Neuron
from neural_network.layer import Layer

from .neuron_type_enum import NeuronTypeEnum


class ExtendedNeuralNetwork(NeuralNetwork):
	def __init__(self, neuron_type: Type[Neuron], input_count, layer_sizes: List[int], name = "New net"):
		super().__init__(neuron_type, input_count, layer_sizes)
		self.name: str = name

	def __getstate__(self):
		return {
			'name': self.name,
			'input_count': self.input_count,
			'layers': [{
				'neuron_type': NeuronTypeEnum(type(layer.neurons[0])).name,
				'weight_matrix': [neuron.weights for neuron in layer.neurons]
			} for layer in self.layers]
		}

	def __setstate__(self, state):
		layers = []
		for layer_state in state['layers']:
			neurons = []
			for weights in range(layer_state['weight_matrix'].shape[1]):
				neuron = NeuronTypeEnum[layer_state['neuron_type']].value(weights.size)
				neuron.weights = weights
			layers.append(Layer.create_from_neurons(neurons))

		self.layers = layers


class NetJsonEnconder(JSONEncoder):
	def default(self, obj: ExtendedNeuralNetwork):
		if isinstance(obj, ExtendedNeuralNetwork):
			return obj.__dict__
		elif isinstance(obj, Layer):
			return {
				'neuron_type': NeuronTypeEnum(type(obj.neurons[0])).name,
				'weight_matrix': [neuron.weights.tolist() for neuron in obj.neurons],
				'biases': [neuron.bias for neuron in obj.neurons]
			}
		return super().default()


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
			neurons = []
			for i, weights in enumerate(dict['weight_matrix']):
				neuron = NeuronTypeEnum[dict['neuron_type']].value(len(weights))
				neuron.weights = numpy.array(weights)
				neuron.bias = dict['biases'][i]
				neurons.append(neuron)
			return Layer.create_from_neurons(neurons)
