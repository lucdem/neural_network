from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List

from .data_point import DataPoint


class Data(ABC):
	@abstractmethod
	def split_batches(self, batch_size: int) -> Iterable[DataSample]:
		pass


class DataSample:
	def __init__(self, data_points: List[DataPoint]):
		DataSample.__validate_data_points(data_points)
		self.data_points = data_points

	@property
	def size(self):
		return len(self.data_points)

	@property
	def input_count(self):
		return len(self.data_points[0].flat_input)

	@property
	def output_count(self):
		return len(self.data_points[0].expected_output)

	@classmethod
	def __validate_data_points(cls, data_points: List[DataPoint]):
		input_count = len(data_points[0].flat_input)
		output_count = len(data_points[0].expected_output)
		for data in data_points:
			if len(data.flat_input) != input_count:
				raise Exception("Data points with inputs of different sizes included in the same SampleData")
			if len(data.expected_output) != output_count:
				raise Exception("Data points with outputs of different sizes included in the same SampleData")

	def get_input(self) -> Iterable[List[float]]:
		for data_point in self.data_points:
			yield data_point.flat_input

	def get_expected_output(self) -> Iterable[List[float]]:
		for data_point in self.data_points:
			yield data_point.expected_output

	def split_batches(self, batch_size: int) -> Iterable[DataSample]:
		batch_data_points: List[DataPoint] = []
		for data_point in self.data_points:
			batch_data_points.append(data_point)
			if len(batch_data_points) == batch_size:
				yield DataSample(batch_data_points)
				batch_data_points = []
		if len(batch_data_points) > 0:
			yield DataSample(batch_data_points)