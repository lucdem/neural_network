from typing import List

import numpy

from .data_point import DataPoint


class DataBatch:
	def __init__(self, data_points: List[DataPoint]):
		self.__class__.__validate_data_points(data_points)
		self.input: numpy.ndarray = numpy.vstack([dp.input for dp in data_points])
		self.expected_output: numpy.ndarray = numpy.vstack([dp.expected_output for dp in data_points])

	@property
	def size(self):
		return self.input.shape[0]

	@property
	def input_count(self):
		return self.input.size

	@property
	def output_count(self):
		return self.expected_output.size

	@classmethod
	def __validate_data_points(cls, data_points: List[DataPoint]):
		input_count = data_points[0].input.size
		output_count = data_points[0].expected_output.size
		for i in range(1, len(data_points)):
			if data_points[i].input.size != input_count:
				raise Exception("Data points with inputs of different sizes included in the same SampleData")
			if data_points[i].expected_output.size != output_count:
				raise Exception("Data points with outputs of different sizes included in the same SampleData")