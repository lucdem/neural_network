from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from app import NetManager, TrainingParams
from .net_params_box import NetParamsBox
from .layer_params_box import LayerParamsBox
from .training_params_box import TrainingParamsBox
from .data_set_box import DataSetBox


class NetContextWidget(QWidget):
	net_built_signal = pyqtSignal(int)

	def __init__(self, net_manager: NetManager) -> None:
		super().__init__()

		self.net_manager = net_manager
		self.net_id = net_manager.selected_net_id

		self.training_worker = NetTrainingWorker(net_manager, self.net_id)
		self.training_thread = QThread()
		self.training_worker.moveToThread(self.training_thread)

		layout = QVBoxLayout()

		self.net_params_box = NetParamsBox()
		layout.addWidget(self.net_params_box, stretch=1)

		self.layer_params_box = LayerParamsBox()
		layout.addWidget(self.layer_params_box, stretch=1)

		self.training_params_box = TrainingParamsBox()
		layout.addWidget(self.training_params_box, stretch=1)

		data_sets_widget = QWidget()
		data_sets_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)
		data_sets_widget.setLayout(QHBoxLayout())
		data_sets_widget.layout().setSpacing(5)
		data_sets_widget.layout().setContentsMargins(0, 0, 0, 0)
		self.training_data_box = DataSetBox("Training Set")
		self.validation_data_box = DataSetBox("Validation Set")
		data_sets_widget.layout().addWidget(self.training_data_box)
		data_sets_widget.layout().addWidget(self.validation_data_box)
		layout.addWidget(data_sets_widget, stretch=1)

		self.setLayout(layout)

		# event/signal bindings

		self.net_params_box.input_count_input.valueChanged.connect(self.layer_params_box.set_input_layer_size)
		self.net_params_box.output_count_input.valueChanged.connect(self.layer_params_box.set_output_layer_size)
		self.net_params_box.hidden_layer_count_input.valueChanged.connect(self.layer_params_box.change_hidden_layer_count)

		self.net_params_box.build_net_button.clicked.connect(self.build_net)
		self.net_params_box.start_training_button.clicked.connect(self.train_net)
		self.net_params_box.stop_training_button.clicked.connect(self.stop_training)

		self.training_thread.started.connect(self.training_worker.start)
		self.training_worker.finished.connect(self.training_thread.quit)
		self.training_worker.finished.connect(self.stop_training)

		self._check_values()

	def build_net(self):
		input_count = self.net_params_box.input_count_input.value()
		layer_sizes = self.layer_params_box.get_layer_sizes()
		layer_types = self.layer_params_box.get_layer_types()
		self.net_manager.build_net(self.net_id, input_count, layer_sizes, layer_types)
		self.net_built_signal.emit(self.net_id)

	def train_net(self):
		self.net_params_box.build_net_button.setEnabled(False)
		self.net_params_box.start_training_button.setEnabled(False)
		self.net_params_box.stop_training_button.setEnabled(True)

		training_data_path = self.training_data_box.file_path_input.text()
		validation_data_path = self.validation_data_box.file_path_input.text()
		training_params = self.training_params_box.get_params()

		self.training_worker.setup(training_data_path, validation_data_path, training_params)
		self.training_thread.start()

	def stop_training(self):
		self.net_params_box.build_net_button.setEnabled(True)
		self.net_params_box.start_training_button.setEnabled(True)
		self.net_params_box.stop_training_button.setEnabled(False)

		self.training_worker.stop = True

	def _check_values(self):
		net = self.net_manager.net_by_id[self.net_id]
		self.net_params_box._check_values(self.net_manager.net_by_id[self.net_id])
		if net.layer_count > 0:
			self.layer_params_box._check_values(self.net_manager.net_by_id[self.net_id].layers)


class NetTrainingWorker(QObject):
	started = pyqtSignal(int, int)
	progress = pyqtSignal(int, int, float, float)
	finished = pyqtSignal(int)

	def __init__(self, net_manager: NetManager, net_id: int) -> None:
		super().__init__()
		self.net_manager = net_manager
		self.net_id = net_id
		self.stop = False

	def setup(self, training_data_path, validation_data_path, training_params):
		self.training_data_path = training_data_path
		self.validation_data_path = validation_data_path
		self.training_params = training_params
		self.stop = False

	def start(self):
		self.started.emit(self.net_id, self.training_params.max_epochs)
		for epoch, cost, acc in self.net_manager.train_net(self.net_id, self.training_data_path,
			self.validation_data_path, self.training_params):

			if self.stop:
				self.stop = False
				break
			self.progress.emit(self.net_id, epoch, cost, acc)
		self.finished.emit(self.net_id)