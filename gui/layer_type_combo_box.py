from PyQt5.QtWidgets import QComboBox

from app import NeuronTypeEnum


class LayerTypeComboBox(QComboBox):
	def __init__(self, initial_type: NeuronTypeEnum = None):
		super().__init__()

		for name, member in NeuronTypeEnum.__members__.items():
			self.addItem(name, member.value)

		if initial_type is not None:
			self.setCurrentIndex(self.findData(initial_type))