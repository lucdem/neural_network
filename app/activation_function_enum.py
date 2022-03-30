from enum import Enum

from neural_network import Logistic, Tanh, ReLU, LeakyReLU, Linear


class ActivationFunctionEnum(Enum):
	Logistic = Logistic
	Tanh = Tanh
	ReLU = ReLU
	LeakyReLU = LeakyReLU
	Linear = Linear