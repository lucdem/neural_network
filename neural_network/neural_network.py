from __future__ import annotations
from typing import List, Type, Tuple, TypeVar

import numpy

from neural_network.data.data_point import DataPoint

from .neuron import Neuron, SigmoidLogisticNeuron
from .layer import Layer
from .cost_function import CostFunction, MeanSquareError
from .data.data import Data, DataSample
from .reverse_list_enumerate import reverse_list_enumerate


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

	def output(self, input: numpy.ndarray) -> Tuple[List[numpy.ndarray], List[numpy.ndarray]]:
		all_layers_outputs: List[numpy.ndarray] = []
		all_layers_zs: List[numpy.ndarray] = []
		layer_input = input
		for layer in self.layers:
			layer_output, z_vector = layer.output(layer_input)
			all_layers_outputs.append(layer_output)
			all_layers_zs.append(z_vector)
			layer_input = layer_output
		return all_layers_outputs, all_layers_zs

	def train(self, epochs: int, learning_rate: float, batch_size: int,
		training_data: Data, cost_function: Type[CostFunction] = MeanSquareError):

		training_batches = training_data.split_batches(batch_size)
		for i in range(epochs):
			for batch in training_batches:
				w, b = self.__train_batch(batch, learning_rate, cost_function)

	def validate(self, validation_data: Data, cost_function: CostFunction) -> Tuple[float, float]:
		data_points = validation_data.get_data_points()
		cost_func_errors = numpy.zeros(len(data_points))
		correct_classification = 0
		for i, data_point in enumerate(data_points):
			output = self.output(data_point.input)[0][-1]
			cost_func_errors[i] = numpy.average(cost_function.func(output, data_point.expected_output, 1))
			if numpy.argmax(output) == numpy.argmax(data_point.expected_output):
				correct_classification += 1
		return numpy.average(cost_func_errors), (correct_classification / len(data_points)) * 100

	def __train_batch(self, batch: DataSample, learning_rate: float, cost_function: Type[CostFunction]):

		all_layers_weight_changes: List[numpy.ndarray] = [numpy.zeros((l.size, l.input_count)) for l in self.layers]
		all_layers_deltas: List[numpy.ndarray] = [numpy.zeros(l.size) for l in self.layers]

		for data_point in batch.data_points:
			all_layers_outputs, all_layers_zs = self.output(data_point.input)
			next_layer_delta = numpy.array([]) # initializing variable, self.__layer_changes ignores this value for output_layer
			for layer_index, layer in reverse_list_enumerate(self.layers):
				weight_changes, delta = self.__calculate_layer_weight_changes(layer_index, data_point, all_layers_outputs,
					all_layers_zs, next_layer_delta, cost_function, batch.size)
				all_layers_weight_changes[layer_index] = all_layers_weight_changes[layer_index] + weight_changes
				all_layers_deltas[layer_index] = all_layers_deltas[layer_index] + delta
				next_layer_delta = delta

		for layer_index, layer in enumerate(self.layers):
			layer.update(all_layers_weight_changes[layer_index], all_layers_deltas[layer_index], learning_rate)

		return all_layers_weight_changes, all_layers_deltas

	def __calculate_layer_weight_changes(self, layer_index, data_point: DataPoint, all_layer_outputs: List[numpy.ndarray],
		all_layer_zs: List[numpy.ndarray], next_layer_delta: numpy.ndarray,
		cost_function, batch_size) -> Tuple[numpy.ndarray, numpy.ndarray]:

		if layer_index == -1: # output layer
			delta = self.layers[layer_index].calculate_output_layer_delta(cost_function, all_layer_outputs[layer_index],
				data_point.expected_output, all_layer_zs[layer_index], batch_size)
		else:
			delta = self.layers[layer_index].calculate_layer_delta(all_layer_zs[layer_index],
				self.layers[layer_index + 1], next_layer_delta)

		if layer_index == -self.layer_count: # first layer
			previous_layer_output = numpy.array([data_point.input])
		else:
			previous_layer_output = numpy.array([all_layer_outputs[layer_index - 1]])

		layer_weight_changes = numpy.array([delta]).T @ previous_layer_output

		return layer_weight_changes, delta