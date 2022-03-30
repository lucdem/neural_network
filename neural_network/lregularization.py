from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np


class LRegularization(ABC):
	def __init__(self, reg_lambda: float):
		self.reg_lambda = reg_lambda

	def cost_term(self, weight_matrices: Iterable[np.ndarray]) -> float:
		return self._cost_term(weight_matrices) * self.reg_lambda

	@abstractmethod
	def _cost_term(self, weight_matrices: Iterable[np.ndarray]) -> float:
		pass

	def weight_update_term(self, weights: np.ndarray) -> np.ndarray:
		return self._weight_update_term(weights) * self.reg_lambda

	@abstractmethod
	def _weight_update_term(self, weights: np.ndarray) -> np.ndarray:
		pass


class L1(LRegularization):
	def _cost_term(self, weight_matrices: Iterable[np.ndarray]) -> float:
		return np.sum([np.sum(np.absolute(matrix)) for matrix in weight_matrices])

	def _weight_update_term(self, weights: np.ndarray) -> np.ndarray:
		return np.where(weights > 0, 1, -1)


class L2(LRegularization):
	def _cost_term(self, weight_matrices: Iterable[np.ndarray]) -> float:
		return np.sum([np.sum(np.absolute(matrix)) for matrix in weight_matrices]) / 2

	def _weight_update_term(self, weights: np.ndarray) -> np.ndarray:
		return weights
