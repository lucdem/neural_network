from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox
from PyQt5.QtCore import Qt

from .qt_helper import get_text_width
from .settings import Settings, SettingsEnum


class OptionsModal(QDialog):
	def __init__(self):
		super().__init__()
		self.setModal(True)
		self.setWindowTitle("Options")

		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
		self.setMinimumWidth(get_text_width(self.windowTitle()) + 100)
		self.setLayout(QGridLayout())

		settings = Settings()

		self.layout().addWidget(QLabel("Line Width"))
		self.graph_line_width_input = QSpinBox()
		self.graph_line_width_input.setRange(1, 10)
		self.graph_line_width_input.setSingleStep(1)
		self.graph_line_width_input.setValue(settings.get_setting(SettingsEnum.GraphLineWidth, int))
		# self.graph_line_width_input.setValue(1)
		self.layout().addWidget(self.graph_line_width_input)

		self.layout().addWidget(QLabel("Update Interval"))
		self.graph_update_interval = QSpinBox()
		self.graph_update_interval.setRange(1, 100)
		self.graph_update_interval.setSingleStep(1)
		self.graph_update_interval.setValue(settings.get_setting(SettingsEnum.GraphUpdateInterval, int))
		# self.graph_update_interval.setValue(5)
		self.layout().addWidget(self.graph_update_interval)