from enum import Enum

from neural_network import MeanSquareError, AbsoluteError


class CostFunctionEnum(Enum):
	MeanSquareError = MeanSquareError
	AbsoluteError = AbsoluteError