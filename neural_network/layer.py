from __future__ import annotations
from typing import List, Tuple, Type

from .neuron import Neuron, SigmoidLogisticNeuron


class Layer:
	def __init__(self, neuron_type: Type[Neuron], input_count, size):
		self.neurons: List[Neuron] = []
		for i in range(size):
			self.neurons.append(neuron_type(input_count))

	@staticmethod
	def create_from_neurons(neurons: List[Neuron]) -> Layer:
		layer = Layer(SigmoidLogisticNeuron, 0, 0)
		layer.neurons = neurons
		return layer

	@property
	def input_count(self):
		return self.neurons[0].input_count

	@property
	def size(self):
		return len(self.neurons)

	def output(self, input) -> Tuple[List[float], List[float]]:
		output: List[float] = [0] * self.size
		z: List[float] = [0] * self.size
		for i, neuron in enumerate(self.neurons):
			output[i], z[i] = neuron.output(input)
		return output, z

	def activation_derivative(self, z) -> List[float]:
		derivative: List[float] = [0] * self.size
		for i, neuron in enumerate(self.neurons):
			derivative[i] = neuron.__class__.activation_derivative(z[i])
		return derivative

	def update(self, weight_changes: List[List[float]], delta: List[float], learning_rate: float):
		for i, neuron in enumerate(self.neurons):
			neuron.update(weight_changes[i], delta[i], learning_rate)