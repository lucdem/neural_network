from __future__ import annotations
from typing import Tuple, Type, Optional

import numpy as np

from .activation_function import ActivationFunction
from .lregularization import LRegularization


class Layer:
	random_bias_std_dev = 0.5
	random_weight_std_dev = 0.5

	def __init__(self, activation_function: Type[ActivationFunction], input_count, size):
		self.activation_function = activation_function
		self.weight_matrix = np.random.normal(0, self.__class__.random_weight_std_dev, (size, input_count))
		self.weights_momentum = np.zeros((size, input_count))
		self.biases = np.random.normal(0, self.__class__.random_weight_std_dev, (size, 1))
		self.biases_momentum = np.zeros((size, 1))

	@property
	def input_count(self):
		return self.weight_matrix.shape[1]

	@property
	def size(self):
		return self.weight_matrix.shape[0]

	def output(self, input) -> Tuple[np.ndarray, np.ndarray]:
		z = (input @ self.weight_matrix.T) + self.biases.T
		output = self.activation_function.activation(z)
		return output, z

	def activation_derivative(self, zs: np.ndarray) -> np.ndarray:
		return self.activation_function.activation_derivative(zs)

	def update(self, weight_derivatives: np.ndarray, delta: np.ndarray, learning_rate: float,
		neuron_drops: Optional[np.ndarray], friction: Optional[float], lregularization: Optional[LRegularization]):

		regularization_term = np.zeros(self.weight_matrix.shape)
		if lregularization is not None:
			regularization_term = lregularization.weight_update_term(self.weight_matrix)

		weights_changes = - ((weight_derivatives + regularization_term) * learning_rate)
		biases_changes = - (delta * learning_rate)

		if neuron_drops is not None:
			weights_changes = weights_changes * neuron_drops
			biases_changes = biases_changes * neuron_drops

		if friction is None:
			self.weight_matrix = self.weight_matrix + weights_changes
			biases_changes = self.biases + biases_changes
		else:
			self.weights_momentum = (self.weights_momentum * (1 - friction)) + weights_changes
			self.weight_matrix = self.weight_matrix + self.weights_momentum
			self.biases_momentum = (self.biases_momentum * (1 - friction)) + biases_changes
			self.biases = self.biases + self.biases_momentum
