from __future__ import annotations
from typing import List, Tuple, Type, Optional

import numpy

from .neuron import Neuron, SigmoidLogisticNeuron
from .cost_function import CostFunction
from .lregularization import LRegularization


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

	@property
	def weight_matrix(self) -> numpy.ndarray:
		return numpy.vstack([n.weights for n in self.neurons])

	def output(self, input) -> Tuple[numpy.ndarray, numpy.ndarray]:
		shape = (input.shape[0], self.size)
		output = numpy.zeros(shape)
		z = numpy.zeros(shape)
		for i, neuron in enumerate(self.neurons):
			output[:, i], z[:, i] = neuron.output(input)
		return output, z

	# generic version for n dimensions, might be useful later
	# def activation_derivative(self, zs: numpy.ndarray) -> numpy.ndarray:
	# 	derivative = numpy.zeros(zs.shape)
	# 	slice_index_list: List[slice | int] = [slice(None) for i in range(zs.ndim)]
	# 	for i, neuron in enumerate(self.neurons):
	# 		slice_index_list[1] = i
	# 		slice_index = tuple(slice_index_list)
	# 		derivative[slice_index] = neuron.__class__.activation_derivative(zs[slice_index])
	# 	return derivative

	def activation_derivative(self, zs: numpy.ndarray) -> numpy.ndarray:
		derivative = numpy.zeros(zs.shape)
		for i, neuron in enumerate(self.neurons):
			derivative[:, i] = neuron.__class__.activation_derivative(zs[:, i])
		return derivative

	def update(self, weight_changes: numpy.ndarray, delta: numpy.ndarray,
		learning_rate: float, friction: Optional[float], lregularization: Optional[LRegularization]):
		"""
		Update neurons in the layer (indexing: [neuron_index, weight_index])

		Keyword Arguments:

			weight_changes -- Values to be subtracted from the weights (before momentum and lregularization is applied),
			indexed as [neuron_index, weight_index]

			delta -- Values to be subtracted from the biases (before momentum and lregularization is applied)
		"""

		for i, neuron in enumerate(self.neurons):
			neuron.update(weight_changes[i, :], delta[i], learning_rate, friction, lregularization)