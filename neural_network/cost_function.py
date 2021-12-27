from abc import ABC, abstractmethod

import numpy


class CostFunction(ABC):
	@classmethod
	@abstractmethod
	def func(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		pass

	@classmethod
	@abstractmethod
	def derivative(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		""" Derivative of the cost function
			relative to the activation function
		"""
		pass


class MeanSquareError(CostFunction):
	@classmethod
	def func(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		return (values - expected_values)**2 / values.shape[0]

	@classmethod
	def derivative(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		return 2 * (values - expected_values) / values.shape[0]


class AbsoluteError(CostFunction):
	@classmethod
	def func(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		return numpy.absolute(values - expected_values)

	@classmethod
	def derivative(cls, values: numpy.ndarray, expected_values: numpy.ndarray) -> numpy.ndarray:
		error = values - expected_values
		error[error < 0] = -1
		error[error > 0] = 1
		return error