from PyQt5.QtWidgets import QComboBox

from app import ActivationFunctionEnum


class LayerTypeComboBox(QComboBox):
	def __init__(self, initial_type: ActivationFunctionEnum = None):
		super().__init__()

		for name, member in ActivationFunctionEnum.__members__.items():
			self.addItem(name, member)

		if initial_type is not None:
			self.set_selected_type(initial_type)

	def get_selected_type(self) -> ActivationFunctionEnum:
		return self.currentData()

	def set_selected_type(self, type: ActivationFunctionEnum):
		self.setCurrentIndex(self.findData(type))