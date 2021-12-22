from __future__ import annotations
from math import exp, tanh
from random import uniform
from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

import numpy

from .lregularization import LRegularization


__T = TypeVar('__T', bound= 'Neuron')


class Neuron(ABC):
	# random_bias_std_dev: float = 0.5
	# random_weight_std_dev: float = 0.5
	random_weight_lower_limit = -0.5
	random_weight_upper_limit = 0.5
	random_bias_lower_limit = 0.5
	random_bias_upper_limit = -0.5

	def __init__(self, input_count: int):
		weights = numpy.zeros(input_count)
		for i in range(input_count):
			weights[i] = uniform(self.__class__.random_weight_lower_limit, self.__class__.random_weight_upper_limit)
		self.weights: numpy.ndarray = weights
		self.bias: float = uniform(self.__class__.random_bias_lower_limit, self.__class__.random_bias_upper_limit)

		self.weight_momentum = numpy.zeros(input_count)
		self.bias_momentum = 0.0

	@property
	def input_count(self):
		return self.weights.size

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

	def z(self, input: numpy.ndarray):
		return self.bias + numpy.dot(input, self.weights)

	def output(self, input: numpy.ndarray) -> Tuple[float, float]:
		z = self.z(input)
		return self.__class__.activation(z), z

	def update(self, weight_changes: numpy.ndarray, delta: float, learning_rate: float,
		friction: float, lregularization: LRegularization):

		if lregularization is not None:
			weight_changes = weight_changes + lregularization.weight_update_term(self.weights)

		if friction is None:
			self.weights = numpy.subtract(self.weights, weight_changes * learning_rate)
			self.bias -= delta * learning_rate
		else:
			self.weight_momentum = numpy.add(self.weight_momentum * (1 - friction), weight_changes * learning_rate)
			self.weights = numpy.subtract(self.weights, self.weight_momentum)
			self.bias_momentum = self.bias_momentum * (1 - friction) + delta * learning_rate
			self.bias -= self.bias_momentum


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