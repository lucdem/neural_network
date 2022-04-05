from PyQt5.QtWidgets import QMainWindow

from app.net_manager import NetManager
from gui.plotting.graphics_wrapper import GraphicsWrapper

from .main_central_widget import MainCentralWidget
from .options_modal import OptionsModal
from .tool_bar import ToolBar
from .settings import Settings, SettingsEnum


class MainWindow(QMainWindow):
	def __init__(self, net_manager: NetManager):
		super().__init__()
		self.settings = Settings()
		self.setWindowTitle("Neural Network")
		self._centralWidget = MainCentralWidget(net_manager) # just to keep static typing
		self.setCentralWidget(self._centralWidget)

		self.toolBar = ToolBar("Settings")
		self.addToolBar(self.toolBar)
		self.options_modal = OptionsModal()

		# event/signal bindings

		self.toolBar.options_action.triggered.connect(self.open_options)

		self.options_modal.graph_line_width_input.valueChanged.connect(self.change_graph_line_width)
		self.options_modal.graph_update_interval.valueChanged.connect(self.change_graph_update_interval)

	def open_options(self):
		self.options_modal.show()

	def change_graph_line_width(self, x: int):
		self._centralWidget.graph_wrapper.line_width = x
		self.settings.change_setting(SettingsEnum.GraphLineWidth, x)

	def change_graph_update_interval(self, x: int):
		GraphicsWrapper.update_interval = x
		self.settings.change_setting(SettingsEnum.GraphUpdateInterval, x)