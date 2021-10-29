from enum import IntEnum, auto


class NeuronTypeEnum(IntEnum):
	Logistic = auto()
	Tanh = auto()
	ReLU = auto()
	LeakyReLU = auto()
	Identity = auto()