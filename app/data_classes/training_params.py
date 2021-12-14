class TrainingParams:
	def __init__(self, training_data_path: str, validation_data_path: str,
			learning_rate: float, friction: float, batch_size: int, max_epochs: int):
		self.training_data_path = training_data_path
		self.validation_data_path = validation_data_path
		self.learning_rate = learning_rate
		self.friction = friction
		self.batch_size = batch_size
		self.max_epochs = max_epochs
