from typing import List, Any

import numpy


class DataPoint:
	def __init__(self, input: List[Any], expected_output: List[float]):
		self.input: numpy.ndarray = numpy.array(input)
		self.expected_output: numpy.ndarray = numpy.array(expected_output)
		self.dimensions = self.input.shape

	@classmethod
	def fromDict(cls, d):
		return DataPoint(d["input"], d["expected_output"])

	@property
	def flat_input(self):
		return numpy.matrix.flatten(self.input)