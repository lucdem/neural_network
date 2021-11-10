from typing import List, Any, Iterable


class DataPoint:
	def __init__(self, input: List[Any], expected_output: List[float]):
		self.input = input
		self.expected_output = expected_output
		self.dimensions: List[int] = []
		x = input[0]
		while isinstance(x, List):
			self.dimensions.append(len(x))
			x = x[0]

	@classmethod
	def fromDict(cls, d):
		return DataPoint(d["input"], d["expected_output"])

	@property
	def flat_input(self):
		return list(DataPoint.__flatten(self.input))

	@classmethod
	def __flatten(cls, l: List[Any]) -> Iterable[float]:
		for ele in l:
			if isinstance(ele, List):
				for nested_ele in DataPoint.__flatten(ele):
					yield nested_ele
			else:
				yield ele