from typing import Type, List

from neural_network import NeuralNetwork, Neuron


class ExtendedNeuralNetwork(NeuralNetwork):
	def __init__(self, name, neuron_type: Type[Neuron], input_count, layer_sizes: List[int]):
		super().__init__(neuron_type, input_count, layer_sizes)
		self.name = name