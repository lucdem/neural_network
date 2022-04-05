from __future__ import annotations
from enum import Enum
from typing import Type

from PyQt5.QtCore import QSettings


class Settings(QSettings):
	def __init__(self):
		super().__init__("settings.ini", QSettings.IniFormat)
		for s in SettingsEnum:
			if not self.contains(s.value):
				self.setValue(s.value, 1)

	def change_setting(self, setting: SettingsEnum, new_value):
		self.setValue(setting.value, new_value)

	def get_setting(self, setting: SettingsEnum, type: type):
		return self.value(setting.value, type = type)


class SettingsEnum(Enum):
	GraphLineWidth = 'Graph/line_width'
	GraphUpdateInterval = 'Graph/update_interval'