from __future__ import annotations
from math import exp, isnan, tanh, isinf
from random import uniform
from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

from .matrix import vec_element_wise_multiplication


__T = TypeVar('__T', bound= 'Neuron')


class Neuron(ABC):
	# random_bias_std_dev: float = 0.5
	# random_weight_std_dev: float = 0.5
	random_weight_lower_limit = -0.5
	random_weight_upper_limit = 0.5
	random_bias_lower_limit = 0.5
	random_bias_upper_limit = -0.5

	def __init__(self, input_count: int):
		weights = [0.0] * input_count
		for i in range(input_count):
			weights[i] = uniform(self.__class__.random_weight_lower_limit, self.__class__.random_weight_upper_limit)
		self.weights: List[float] = weights
		self.bias: float = uniform(self.__class__.random_bias_lower_limit, self.__class__.random_bias_upper_limit)

	@property
	def input_count(self):
		return len(self.weights)

	@classmethod
	@abstractmethod
	def activation(cls, z) -> float:
		"""z is the sum of weighted inputs plus the bias"""
		pass

	@classmethod
	@abstractmethod
	def activation_derivative(cls, z) -> float:
		"""Derivative of the activation function relative to z,
			where z is the sum of weighted inputs plus the bias
		"""
		pass

	def z(self, input):
		return self.bias + sum(vec_element_wise_multiplication(input, self.weights))

	def output(self, input: List[float]) -> Tuple[float, float]:
		z = self.z(input)
		return self.__class__.activation(z), z

	def update(self, weight_changes: List[float], delta: float, learning_rate: float):
		for i, weight_change in enumerate(weight_changes):
			self.weights[i] -= weight_change * learning_rate
		self.bias -= delta * learning_rate
		if any(isinf(w) or isnan(w) for w in self.weights) or isinf(self.bias) or isnan(self.bias):
			raise Exception("Neuron paramters inf or Nan, this is likely due to an exploding gradient problem")

	def add_inputs(self, new_input_count):
		for i in range(new_input_count):
			self.weights.append(uniform(Neuron.random_weight_lower_limit, Neuron.random_weight_upper_limit))


class SigmoidLogisticNeuron(Neuron):
	@classmethod
	def activation(cls, z):
		return 1 / (1 + exp(-z))

	@classmethod
	def activation_derivative(cls, z):
		return exp(z) / (1 + exp(z)) ** 2


class SigmoidTanhNeuron(Neuron):
	@classmethod
	def activation(cls, z):
		return tanh(z)

	@classmethod
	def activation_derivative(cls, z):
		return 1 - tanh(z) ** 2


class ReLU_Neuron(Neuron):
	@classmethod
	def activation(cls, z):
		return 0 if z < 0 else z

	@classmethod
	def activation_derivative(cls, z):
		return 0 if z < 0 else 1


class LeakyReLU_Neuron(Neuron):
	leak_const = 0.01

	@classmethod
	def activation(cls, z):
		return cls.leak_const * z if z < 0 else z

	@classmethod
	def activation_derivative(cls, z):
		return cls.leak_const if z < 0 else 1


class LinearNeuron(Neuron):
	@classmethod
	def activation(cls, z):
		return z

	@classmethod
	def activation_derivative(cls, z):
		return 1