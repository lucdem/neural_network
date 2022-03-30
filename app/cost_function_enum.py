from enum import Enum

from neural_network import SquaredError, AbsoluteError


class CostFunctionEnum(Enum):
	MeanSquareError = SquaredError
	AbsoluteError = AbsoluteError