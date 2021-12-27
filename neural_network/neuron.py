from __future__ import annotations
from random import uniform
from abc import ABC, abstractmethod
from typing import Tuple, TypeVar, Optional

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
		self.weights = numpy.zeros(input_count)
		for i in range(input_count):
			self.weights[i] = uniform(self.__class__.random_weight_lower_limit, self.__class__.random_weight_upper_limit)
		self.bias: float = uniform(self.__class__.random_bias_lower_limit, self.__class__.random_bias_upper_limit)

		self.weight_momentum = numpy.zeros(input_count)
		self.bias_momentum = 0.0

	@property
	def input_count(self):
		return self.weights.size

	@classmethod
	@abstractmethod
	def activation(cls, z: numpy.ndarray) -> float:
		"""z is the sum of weighted inputs plus the bias"""
		pass

	@classmethod
	@abstractmethod
	def activation_derivative(cls, z: numpy.ndarray) -> float:
		"""Derivative of the activation function relative to z, where z is the sum of weighted inputs plus the bias"""
		pass

	def z(self, input: numpy.ndarray):
		return self.bias + numpy.dot(input, self.weights)

	def output(self, input: numpy.ndarray) -> Tuple[float, float]:
		z = self.z(input)
		return self.__class__.activation(z), z

	def update(self, weight_changes: numpy.ndarray, delta: float, learning_rate: float,
		friction: Optional[float], lregularization: Optional[LRegularization]):

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
	def activation(cls, z: numpy.ndarray):
		return 1 / (1 + numpy.exp(-z))

	@classmethod
	def activation_derivative(cls, z: numpy.ndarray):
		return numpy.exp(z) / (1 + numpy.exp(z)) ** 2


class SigmoidTanhNeuron(Neuron):
	@classmethod
	def activation(cls, z: numpy.ndarray):
		return numpy.tanh(z)

	@classmethod
	def activation_derivative(cls, z: numpy.ndarray):
		return 1 - numpy.tanh(z) ** 2


class ReLU_Neuron(Neuron):
	@classmethod
	def activation(cls, z: numpy.ndarray):
		return numpy.where(z < 0, 0, z)

	@classmethod
	def activation_derivative(cls, z: numpy.ndarray):
		return numpy.where(z < 0, 0, 1)


class LeakyReLU_Neuron(Neuron):
	leak_const = 0.01

	@classmethod
	def activation(cls, z: numpy.ndarray):
		return numpy.where(z < 0, z * LeakyReLU_Neuron.leak_const, z)

	@classmethod
	def activation_derivative(cls, z: numpy.ndarray):
		return numpy.where(z < 0, LeakyReLU_Neuron.leak_const, 1)


class LinearNeuron(Neuron):
	@classmethod
	def activation(cls, z: numpy.ndarray):
		return z

	@classmethod
	def activation_derivative(cls, z: numpy.ndarray):
		return numpy.ones(z.shape)