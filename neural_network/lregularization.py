from abc import ABC, abstractmethod
from typing import Iterable

import numpy


class LRegularization(ABC):
	def __init__(self, reg_lambda: float, batch_size: float):
		self.reg_lambda = reg_lambda
		self.batch_size = batch_size

	def cost_term(self, weights_iter: Iterable[numpy.ndarray]) -> float:
		return self._cost_term(weights_iter) * self.reg_lambda

	@abstractmethod
	def _cost_term(self, weights_iter: Iterable[numpy.ndarray]) -> float:
		pass

	def weight_update_term(self, weights: numpy.ndarray) -> numpy.ndarray:
		return self._weight_update_term(weights) * self.reg_lambda / self.batch_size

	@abstractmethod
	def _weight_update_term(self, weights: numpy.ndarray) -> numpy.ndarray:
		pass


class L1(LRegularization):
	def _cost_term(self, weights_iter: Iterable[numpy.ndarray]) -> float:
		cost = 0
		for weight_arr in weights_iter:
			cost += weight_arr.sum()
		return cost

	def _weight_update_term(self, weights: numpy.ndarray) -> numpy.ndarray:
		return numpy.where(weights > 1, 1, -1)


class L2(LRegularization):
	def _cost_term(self, weights_iter: Iterable[numpy.ndarray]) -> float:
		cost = 0
		for weight_arr in weights_iter:
			cost += numpy.square(weight_arr).sum()
		return cost

	def _weight_update_term(self, weights: numpy.ndarray) -> numpy.ndarray:
		return weights * 2