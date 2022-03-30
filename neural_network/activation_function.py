from __future__ import annotations
from abc import ABC, abstractmethod

import numpy as np


class ActivationFunction(ABC):
	@classmethod
	@abstractmethod
	def activation(cls, z: np.ndarray) -> np.ndarray:
		"""z is the sum of weighted inputs plus the bias"""
		pass

	@classmethod
	@abstractmethod
	def activation_derivative(cls, z: np.ndarray) -> np.ndarray:
		"""Derivative of the activation function relative to z, where z is the sum of weighted inputs plus the bias"""
		pass


class Logistic(ActivationFunction):
	@classmethod
	def activation(cls, z: np.ndarray):
		return 1 / (1 + np.exp(-z))

	@classmethod
	def activation_derivative(cls, z: np.ndarray):
		return np.exp(z) / (1 + np.exp(z)) ** 2


class Tanh(ActivationFunction):
	@classmethod
	def activation(cls, z: np.ndarray):
		return np.tanh(z)

	@classmethod
	def activation_derivative(cls, z: np.ndarray):
		return 1 - np.tanh(z) ** 2


class ReLU(ActivationFunction):
	@classmethod
	def activation(cls, z: np.ndarray):
		return np.where(z < 0, 0, z)

	@classmethod
	def activation_derivative(cls, z: np.ndarray):
		return np.where(z < 0, 0, 1)


class LeakyReLU(ActivationFunction):
	leak_const = 0.01

	@classmethod
	def activation(cls, z: np.ndarray):
		return np.where(z < 0, z * cls.leak_const, z)

	@classmethod
	def activation_derivative(cls, z: np.ndarray):
		return np.where(z < 0, cls.leak_const, 1)


class Linear(ActivationFunction):
	@classmethod
	def activation(cls, z: np.ndarray):
		return z

	@classmethod
	def activation_derivative(cls, z: np.ndarray):
		return np.ones(z.shape)