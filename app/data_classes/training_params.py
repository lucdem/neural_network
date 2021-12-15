from typing import Type
from neural_network import CostFunction, MeanSquareError


class TrainingParams:
	def __init__(self, learning_rate: float, friction: float, batch_size: int, max_epochs: int,
		dropout: float, cost_function: Type[CostFunction] = MeanSquareError):
		self.learning_rate = learning_rate
		self.friction = friction
		self.batch_size = batch_size
		self.max_epochs = max_epochs
		self.dropout = dropout
		self.cost_function = cost_function