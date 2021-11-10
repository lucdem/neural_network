from __future__ import annotations
from typing import List, Type, Tuple, Union

from .neuron import Neuron, SigmoidLogisticNeuron
from .layer import Layer
from .cost_function import CostFunction, MeanSquareError
from .data.data import Data, DataSample
from .reverse_list_enumerate import reverse_list_enumerate
from .matrix import vec_element_wise_multiplication, matrix_sum, vec_sum


class NeuralNetwork:
	def __init__(self, neuron_type: Type[Neuron], input_count, layer_sizes: List[int]):
		self.layers = [Layer(neuron_type, input_count, layer_sizes[0])]
		for i in range(1, len(layer_sizes)):
			self.layers.append(Layer(neuron_type, layer_sizes[i - 1], layer_sizes[i]))

	@classmethod
	def create_from_layers(cls, layers: List[Layer]) -> NeuralNetwork:
		net = NeuralNetwork(SigmoidLogisticNeuron, 0, [0])
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
			return self.layers[0].size
		else:
			return 0

	def output(self, input: List[float]) -> Tuple[List[List[float]], List[List[float]]]:
		all_layer_output: List[List[float]] = []
		all_layer_z_vectors: List[List[float]] = []
		layer_input = input
		for layer in self.layers:
			layer_output, z_vector = layer.output(layer_input)
			all_layer_output.append(layer_output)
			all_layer_z_vectors.append(z_vector)
			layer_input = layer_output
		return all_layer_output, all_layer_z_vectors

	def train(self, epochs: int, learning_rate: float, batch_size: int,
		training_data: Data, validation_data: Data = None,
		cost_function: Type[CostFunction] = MeanSquareError):

		training_batches = training_data.split_batches(batch_size)

		for i in range(epochs):
			for batch in training_batches:
				w, b = self.__train_batch(batch, learning_rate, cost_function)
				# debug = 1

		# TODO: validation

	def __train_batch(self, batch: DataSample, learning_rate: float, cost_function: Type[CostFunction]):
		all_layer_weight_changes: List[List[List[float]]] = []
		all_layer_deltas: List[List[float]] = []

		for data_point_index, data_point in enumerate(batch.data_points):
			all_layer_outputs, all_layer_zs = self.output(data_point.flat_input)
			next_layer_delta = 1 # initializing variable, self.__layer_changes ignores this value for output_layer
			for layer_index, layer in reverse_list_enumerate(self.layers):
				weight_changes, delta = self.__layer_changes(layer_index, data_point, all_layer_outputs,
					all_layer_zs, next_layer_delta, cost_function, batch.size)
				if data_point_index == 0:
					all_layer_weight_changes.append(weight_changes)
					all_layer_deltas.append(delta)
					if len(all_layer_weight_changes) == self.layer_count:
						all_layer_weight_changes.reverse()
						all_layer_deltas.reverse()
				else:
					all_layer_weight_changes[layer_index] = matrix_sum(all_layer_weight_changes[layer_index], weight_changes)
					all_layer_deltas[layer_index] = vec_sum(all_layer_deltas[layer_index], delta)
				next_layer_delta = delta

		for layer_index, layer in enumerate(self.layers):
			layer.update(all_layer_weight_changes[layer_index], all_layer_deltas[layer_index], learning_rate)

		return all_layer_weight_changes, all_layer_deltas

	def __layer_changes(self, layer_index, data_point, all_layer_outputs,
		all_layer_zs, next_layer_delta, cost_function, batch_size):
		if layer_index == -1: # output layer
			delta = self.__output_layer_delta(cost_function, all_layer_outputs[-1],
				data_point.expected_output, batch_size, all_layer_zs[-1])
		else:
			delta = self.__layer_delta(layer_index, all_layer_zs[layer_index], next_layer_delta)

		if layer_index == -self.layer_count: # first layer
			previous_layer_output = data_point.flat_input
		else:
			previous_layer_output = all_layer_outputs[layer_index - 1]

		layer_weight_changes: List[List[float]] = []
		for i, neuron in enumerate(self.layers[layer_index].neurons):
			neuron_weight_changes = [0] * neuron.input_count
			for k, input in enumerate(previous_layer_output):
				neuron_weight_changes[k] = input * delta[i]
			layer_weight_changes.append(neuron_weight_changes)

		return layer_weight_changes, delta

	def __output_layer_delta(self, cost_function, output, expected_output,
		batch_size, layer_z) -> List[float]:
		cost_function_derivative = cost_function.derivative(output, expected_output, batch_size)
		return vec_element_wise_multiplication(cost_function_derivative, self.layers[-1].activation_derivative(layer_z))

	def __layer_delta(self, layer_index, layer_z, next_layer_delta) -> List[float]:
		layer = self.layers[layer_index]
		next_layer = self.layers[layer_index + 1]
		layer_delta = [0.0] * layer.size
		layer_derivatives = self.layers[layer_index].activation_derivative(layer_z)
		for i in range(layer.size):
			for k, next_layer_neuron_delta in enumerate(next_layer_delta):
				layer_delta[i] += next_layer_neuron_delta * next_layer.neurons[k].weights[i]
		return vec_element_wise_multiplication(layer_derivatives, layer_delta)

	def classification_accuracy(self, validation_data: DataSample) -> float:
		successes = 0
		for data in validation_data.data_points:
			output = self.output(data.flat_input)[0][-1]

			classification = 0
			biggest = float('-inf')
			for i, value in enumerate(output):
				if value > biggest:
					biggest = value
					classification = i

			expected_classification = 0
			biggest = float('-inf')
			for i, value in enumerate(data.expected_output):
				if value > biggest:
					biggest = value
					expected_classification = i

			if classification != expected_classification:
				successes += 1
		return successes / validation_data.size