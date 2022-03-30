from typing import Iterable
from PyQt5.QtWidgets import QPlainTextEdit

from app import NetManager


class TextOutputWidget(QPlainTextEdit):
	def __init__(self, net_manager: NetManager):
		super().__init__()
		self.setReadOnly(True)
		self.setBackgroundVisible(False)

		self.net_manager = net_manager

		self.update_interval = 5	# TODO: some way for the user to change this

	def message(self, msg: str, **kwargs):
		if len(kwargs) > 0:
			msg += f' ### {kwargs}'
		self.appendPlainText(msg)

	def multiline_message(self, msgs: Iterable[str]):
		for msg in msgs:
			self.appendPlainText(msg)

	def net_name_change_msg(self, net_id: int, new_name: str):
		self.message(f'Net name changed to: "{new_name}"')

	def net_built_msg(self, net_id: int):
		self.message(f'Built net: "{self.net_manager.net_by_id[net_id].name}"')

	def training_started_msg(self, net_id: int, max_epochs: int):
		self.message(f'Started Training net: "{self.net_manager.net_by_id[net_id].name}"')

	def training_progress_msg(self, net_id: int, epoch: int, cost: float, acc: float):
		epoch = epoch + 1
		if epoch % self.update_interval == 0:
			self.multiline_message([
				f'Training progress for: "{self.net_manager.net_by_id[net_id].name}"',
				f'\tepoch = {epoch}',
				f'\tcost = {cost}',
				f'\taccuracy = {acc}'
			])