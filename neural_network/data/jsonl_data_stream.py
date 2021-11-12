from __future__ import annotations
import jsonlines
from typing import Iterable

from .data import Data, DataSample
from .data_point import DataPoint


class JsonlDataStream(Data):
	def __init__(self, jsonl_file_path):
		self.file = open(jsonl_file_path)
		self.reader = jsonlines.Reader(self.file)

	def split_batches(self, batch_size: int) -> Iterable[DataSample]:
		""" Randomly distributes data points in batches.
			Last batch can have size smaller than batch_size to contain
			leftover data points
		"""

		batch = []
		while True:
			try:
				batch.append(DataPoint.fromDict(self.reader.read()))
			except EOFError:
				break
			if len(batch) == batch_size:
				yield DataSample(batch)
				batch = []
		if len(batch) > 0:
			yield DataSample(batch)