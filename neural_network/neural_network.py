from __future__ import annotations
from typing import List, Type, Tuple, TypeVar, Optional
from random import uniform
import itertools

import numpy

from neural_network.data.data_point import DataPoint

from .neuron import Neuron, SigmoidLogisticNeuron
from .layer import Layer
from .cost_function import CostFunction
from .data.data import Data
from .data.data_batch import DataBatch
from .reverse_list_enumerate import reverse_list_enumerate
from .lregularization import LRegularization


__T = TypeVar('__T', bound= 'NeuralNetwork')


class NeuralNetwork:
	def __init__(self, neuron_type: Type[Neuron], input_count, layer_sizes: List[int]):
		self.layers = [Layer(neuron_type, input_count, layer_sizes[0])]
		for i in range(1, len(layer_sizes)):
			self.layers.append(Layer(neuron_type, layer_sizes[i - 1], layer_sizes[i]))

	@classmethod
	def create_from_layers(cls: Type[__T], layers: List[Layer]) -> __T:
		net = cls(SigmoidLogisticNeuron, 0, [0])
		net.layers = layers
		return net

	@property
	def layer_count(self):
		return len(self.layers)

	@property
	def output_count(self):
		if self.layer_count > 0:
			return self.layers[-1].size
		else:
			return 0

	@property
	def input_count(self):
		if self.layer_count > 0:
			return self.layers[0].input_count
		else:
			return 0

	def output(self, input: numpy.ndarray,
		neuron_drops: Optional[List[numpy.ndarray]] = None) -> Tuple[List[numpy.ndarray], List[numpy.ndarray]]:

		all_layers_outputs: List[numpy.ndarray] = []
		all_layers_zs: List[numpy.ndarray] = []
		layer_input = input
		for i, layer in enumerate(self.layers):
			layer_output, layer_z = layer.output(layer_input)
			if neuron_drops is not None:
				layer_output = layer_output * neuron_drops[i]
				# equivalent: layer_output = layer_output @ numpy.diag(neuron_drops)
			all_layers_outputs.append(layer_output)
			all_layers_zs.append(layer_z)
			layer_input = layer_output
		return all_layers_outputs, all_layers_zs

	def train(self, epochs: int, learning_rate: float, friction: float,
		batch_size: int, dropout: float, training_data: Data,
		cost_function: Type[CostFunction], lregularization: Optional[LRegularization]):

		training_batches = training_data.split_batches(batch_size)
		for i in range(epochs):
			for batch in training_batches:
				self.__train_batch(batch, learning_rate, friction, dropout, cost_function, lregularization)

	def validate(self, validation_data: Data, cost_function: Type[CostFunction],
		lregularization: LRegularization) -> Tuple[float, float]:

		cost_func_errors = numpy.zeros(len(validation_data.data_points))
		correct_classification = 0
		regularization_cost = 0.0
		if lregularization is not None:
			regularization_cost = lregularization.cost_term(
				itertools.chain.from_iterable(((n.weights for n in l.neurons) for l in self.layers)))
		for i, data_point in enumerate(validation_data.data_points):
			output = self.output(data_point.input)[0][-1]
			cost_func_errors[i] = (numpy.average(cost_function.func(output, data_point.expected_output))
				+ regularization_cost)
			if numpy.argmax(output) == numpy.argmax(data_point.expected_output):
				correct_classification += 1
		return numpy.average(cost_func_errors), (correct_classification / len(validation_data.data_points)) * 100

	def __train_batch(self, batch: DataBatch, learning_rate: float, friction: float,
		dropout: float, cost_function: Type[CostFunction], lregularization: Optional[LRegularization]):

		layers_weight_changes: List[numpy.ndarray] = [numpy.zeros((batch.size, l.size, l.input_count)) for l in self.layers]
		layers_batch_deltas: List[numpy.ndarray] = [numpy.zeros((batch.size, l.size)) for l in self.layers]
		neuron_drops = None
		if dropout > 0:
			neuron_drops = [
				numpy.array([1 if uniform(0, 1) > dropout else 0 for _ in range(layer.size)])
				for layer in self.layers[:self.layer_count - 1]
			]
			neuron_drops.append(numpy.array([1] * self.output_count))

		layers_outputs, layers_zs = self.output(batch.input, neuron_drops)
		next_layer_delta = numpy.array([]) # initializing variable, is ignored for output_layer
		for layer_index, layer in reverse_list_enumerate(self.layers):
			if layer_index == -1:
				batch_delta = self.__calculate_output_layer_delta(cost_function, layers_outputs[layer_index],
					batch.expected_output, layers_zs[layer_index])
			else:
				batch_delta = self.__calculate_layer_delta(layer_index, layers_zs[layer_index], next_layer_delta)
				if neuron_drops is not None:
					batch_delta = numpy.multiply(batch_delta, neuron_drops[layer_index])

			weight_changes = self.__calculate_layer_weight_changes(layer_index, batch, layers_outputs, batch_delta)
			layers_weight_changes[layer_index] = weight_changes
			layers_batch_deltas[layer_index] = batch_delta
			next_layer_delta = batch_delta

		for layer_index, layer in enumerate(self.layers):
			layer.update(layers_weight_changes[layer_index], layers_batch_deltas[layer_index].sum(0),
				learning_rate, friction, lregularization)

	def __calculate_output_layer_delta(self, cost_function: Type[CostFunction],
		output: numpy.ndarray, expected_output: numpy.ndarray,
		layer_z: numpy.ndarray) -> numpy.ndarray:

		cost_function_derivative = cost_function.derivative(output, expected_output)
		return cost_function_derivative * self.layers[-1].activation_derivative(layer_z)

	def __calculate_layer_delta(self, layer_index: int, layer_z: numpy.ndarray,
		next_layer_delta: numpy.ndarray) -> numpy.ndarray:

		layer_derivatives = self.layers[layer_index].activation_derivative(layer_z)
		layer_delta = numpy.vstack([
			next_layer_delta[i, :] @ self.layers[layer_index + 1].weight_matrix
			for i in range(next_layer_delta.shape[0])
		])
		return layer_derivatives * layer_delta

	def __calculate_layer_weight_changes(self, layer_index: int, batch: DataBatch,
		all_layer_outputs: List[numpy.ndarray], delta: numpy.ndarray) -> numpy.ndarray:

		if layer_index == -self.layer_count: # first layer
			previous_layer_output = batch.input
		else:
			previous_layer_output = all_layer_outputs[layer_index - 1]

		layer_weight_changes = delta.T @ previous_layer_output

		return layer_weight_changes