from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Iterable, List

from .data_point import DataPoint


class Data(ABC):
	@abstractproperty
	def get_data_points(self) -> List[DataPoint]:
		pass

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
		return self.data_points[0].input.size

	@property
	def output_count(self):
		return self.data_points[0].expected_output.size

	@property
	def get_data_points(self) -> List[DataPoint]:
		return self.data_points

	@classmethod
	def __validate_data_points(cls, data_points: List[DataPoint]):
		input_count = data_points[0].input.size
		output_count = data_points[0].expected_output.size
		for i in range(1, len(data_points)):
			if data_points[i].input.size != input_count:
				raise Exception("Data points with inputs of different sizes included in the same SampleData")
			if data_points[i].expected_output.size != output_count:
				raise Exception("Data points with outputs of different sizes included in the same SampleData")

	def get_flat_input(self) -> Iterable[List[float]]:
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