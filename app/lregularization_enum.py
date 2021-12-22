from enum import Enum

from neural_network import L1, L2


class LRegularizationEnum(Enum):
	L1 = L1,
	L2 = L2