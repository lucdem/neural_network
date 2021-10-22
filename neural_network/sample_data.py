from __future__ import annotations
from typing import List
from random import randint


class DataPoint:
	def __init__(self, input: List[float], expected_output: List[float]):
		self.input = input
		self.expected_output = expected_output


class SampleData:
	def __init__(self):
		self.data_points: List[DataPoint] = None

	@property
	def size(self):
		return len(self.data_points)

	@property
	def input_count(self):
		return len(self.data_points[0].input)

	@property
	def output_count(self):
		return len(self.data_points[0].expected_output)

	def get_input(self):
		for data_point in self.data_points:
			yield data_point.input

	def get_expected_output(self):
		for data_point in self.data_points:
			yield data_point.expected_output

	@classmethod
	def create_from_lists(cls, inputs: List[List[float]], outputs: List[List[float]]) -> SampleData:
		SampleData.__validate_lists(inputs, outputs)
		size = len(inputs)
		data_points: List[DataPoint] = []
		for i in range(size):
			data_points[i] = DataPoint(inputs[i], outputs[i])
		return SampleData.create_from_data_points(data_points)

	@classmethod
	def create_from_data_points(cls, data_points: List[DataPoint]) -> SampleData:
		SampleData.__validate_data_points(data_points)
		return SampleData.__create_from_data_points(data_points)

	@classmethod
	def __create_from_data_points(cls, data_points: List[DataPoint]) -> SampleData:
		data = SampleData()
		data.data_points = data_points
		return data

	# @classmethod
	# def create_from_csv(cls, file, interpreter):

	# @classmethod
	# def create_from_json(cls, file, interpreter):

	@classmethod
	def __validate_lists(cls, inputs, outputs):
		if len(inputs) != len(outputs):
			raise Exception("number of input data points does not match number of output data points")

	@classmethod
	def __validate_data_points(cls, data_points: List[DataPoint]):
		input_count = len(data_points[0].input)
		output_count = len(data_points[0].expected_output)
		for data in data_points:
			if len(data.input) != input_count:
				raise Exception("Data points with inputs of different sizes included in the same SampleData")
			if len(data.expected_output) != output_count:
				raise Exception("Data points with outputs of different sizes included in the same SampleData")

	# def output_by_index(self, output_index: int) -> Iterator[Tuple[int, float]]:
	# 	for data_point_index, data_point in enumerate(self.data_points):
	# 		yield data_point_index, data_point.expected_output[output_index]

	def split_random_batches(self, batch_size: int) -> List[SampleData]:
		""" Randomly distributes data points in batches.
			First batch can have length up to 2*batch_size-1 to contain
			leftover data points
		"""
		used = [False] * self.size
		batch_count = self.size // batch_size
		batches: List[SampleData] = []

		for i in range(batch_count):
			batch_data_points: List[DataPoint] = []
			for k in range(batch_size):
				chosen = randint(0, self.size - 1)
				while used[chosen]:
					chosen -= 1
				batch_data_points.append(self.data_points[chosen])
				used[chosen] = True
			batches.append(SampleData.__create_from_data_points(batch_data_points))

		if self.size % batch_size != 0:
			for i in range(0, self.size):
				if not used[i]:
					batches[0].data_points.append(self.data_points[i])

		return batches