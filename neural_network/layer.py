from __future__ import annotations
from typing import List, Tuple, Type

import numpy

from .neuron import Neuron, SigmoidLogisticNeuron
from .cost_function import CostFunction


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

	def output(self, input) -> Tuple[numpy.ndarray, numpy.ndarray]:
		output = numpy.zeros(self.size)
		z = numpy.zeros(self.size)
		for i, neuron in enumerate(self.neurons):
			output[i], z[i] = neuron.output(input)
		return output, z

	def activation_derivative(self, zs: numpy.ndarray) -> numpy.ndarray:
		derivative = numpy.zeros(self.size)
		for i, neuron in enumerate(self.neurons):
			derivative[i] = neuron.__class__.activation_derivative(zs[i])
		return derivative

	def update(self, weight_changes: numpy.ndarray, delta: numpy.ndarray, learning_rate: float):
		for i, neuron in enumerate(self.neurons):
			neuron.update(weight_changes[i, :], delta[i], learning_rate)

	def calculate_output_layer_delta(self, cost_function: CostFunction,
		output: numpy.ndarray, expected_output: numpy.ndarray,
		layer_z: numpy.ndarray, batch_size: int) -> numpy.ndarray:

		cost_function_derivative = cost_function.derivative(output, expected_output, batch_size)
		return cost_function_derivative * self.activation_derivative(layer_z)

	def calculate_layer_delta(self, layer_z: numpy.ndarray,
		next_layer: Layer, next_layer_delta: numpy.ndarray) -> numpy.ndarray:

		layer_delta = numpy.zeros(self.size)
		layer_derivatives = self.activation_derivative(layer_z)
		for i in range(next_layer_delta.size):
			layer_delta = layer_delta + next_layer_delta[i] * next_layer.neurons[i].weights
		return layer_derivatives * layer_delta