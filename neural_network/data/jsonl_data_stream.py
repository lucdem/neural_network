from __future__ import annotations
import jsonlines
from typing import Iterable, List

from .data import Data, DataSample
from .data_point import DataPoint


class JsonlDataStream(Data):
	def __init__(self, jsonl_file_path):
		self.file_path = jsonl_file_path

	@property
	def data_points(self) -> List[DataPoint]:
		with jsonlines.Reader(open(self.file_path)) as reader:
			data_points = []
			while True:
				try:
					data_points.append(DataPoint.fromDict(reader.read()))
				except EOFError:
					break
		return data_points

	def split_batches(self, batch_size: int) -> Iterable[DataSample]:
		with jsonlines.Reader(open(self.file_path)) as reader:
			batch = []
			while True:
				try:
					batch.append(DataPoint.fromDict(reader.read()))
				except EOFError:
					break
				if len(batch) == batch_size:
					yield DataSample(batch)
					batch = []
			if len(batch) > 0:
				yield DataSample(batch)