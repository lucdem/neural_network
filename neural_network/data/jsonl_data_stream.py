from __future__ import annotations
import jsonlines
from typing import Iterable, List

from .data import Data
from .data_point import DataPoint
from .data_batch import DataBatch


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

	def split_batches(self, batch_size: int) -> Iterable[DataBatch]:
		with jsonlines.Reader(open(self.file_path)) as reader:
			batch_data_points = []
			while True:
				try:
					batch_data_points.append(DataPoint.fromDict(reader.read()))
				except EOFError:
					break
				if len(batch_data_points) == batch_size:
					yield DataBatch(batch_data_points)
					batch_data_points = []
			if len(batch_data_points) > 0:
				yield DataBatch(batch_data_points)