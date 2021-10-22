from abc import ABC, abstractmethod
from typing import List


def _check_sizes(values, expected_values):
	if len(expected_values) != len(values):
		raise Exception(
			'Expected value and value lists have different sizes')


class CostFunction(ABC):
	@classmethod
	@abstractmethod
	def func(cls, values: list, expected_values: list, n: int) -> List[float]:
		pass

	@classmethod
	@abstractmethod
	def derivative(cls, values: list, expected_values: list, n: int) -> List[float]:
		""" Derivative of the cost function
			relative to the activation function
		"""
		pass


class MeanSquareError(CostFunction):
	@classmethod
	def func(cls, values: list, expected_values: list, n: int):
		_check_sizes(values, expected_values)
		vec_size = len(values)
		squared_error: List[float] = [0] * vec_size
		for i in range(vec_size):
			squared_error[i] = (values[i] - expected_values[i])**2 / n
		return squared_error

	@classmethod
	def derivative(cls, values: list, expected_values: list, n: int):
		_check_sizes(values, expected_values)
		vec_size = len(values)
		squared_error: List[float] = [0] * vec_size
		for i in range(vec_size):
			squared_error[i] = 2 * (values[i] - expected_values[i]) / n
		return squared_error


class AbsoluteError(CostFunction):
	@classmethod
	def func(cls, values: list, expected_values: list, n: int):
		_check_sizes(values, expected_values)
		vec_size = len(values)
		error: List[float] = [0] * vec_size
		for i in range(vec_size):
			error[i] = abs(values[i] - expected_values[i])
		return error

	@classmethod
	def derivative(cls, values: list, expected_values: list, n: int):
		_check_sizes(values, expected_values)
		vec_size = len(values)
		error: List[float] = [0] * vec_size
		for i in range(vec_size):
			error[i] = -1 if (values[i] - expected_values[i]) < 0 else 1
		return error