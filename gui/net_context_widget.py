from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from app import NetManager
from .net_params_box import NetParamsBox
from .layer_params_box import LayerParamsBox
from .training_params_box import TrainingParamsBox
from .data_set_box import DataSetBox


class NetContextWidget(QWidget):
	def __init__(self, net_manager: NetManager) -> None:
		super().__init__()

		self.net_manager = net_manager

		layout = QVBoxLayout()

		self.net_params_box = NetParamsBox()
		layout.addWidget(self.net_params_box, stretch=1)

		self.layer_params_box = LayerParamsBox()
		layout.addWidget(self.layer_params_box, stretch=1)

		self.training_params_box = TrainingParamsBox()
		layout.addWidget(self.training_params_box, stretch=1)

		data_sets_widget = QWidget()
		data_sets_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)
		data_sets_widget.setLayout(QHBoxLayout())
		data_sets_widget.layout().setSpacing(5)
		data_sets_widget.layout().setContentsMargins(0, 0, 0, 0)
		data_sets_widget.layout().addWidget(DataSetBox("Training Set"))
		data_sets_widget.layout().addWidget(DataSetBox("Validation Set"))
		layout.addWidget(data_sets_widget, stretch=1)

		self.setLayout(layout)

		# event/signal bindings

		self.net_params_box.input_count_input.valueChanged.connect(self.layer_params_box.set_input_layer_size)
		self.net_params_box.output_count_input.valueChanged.connect(self.layer_params_box.set_output_layer_size)
		self.net_params_box.hidden_layer_count_input.valueChanged.connect(self.layer_params_box.change_hidden_layer_count)

		self.net_params_box.build_net_button.clicked.connect(self.build_net)
		self.net_params_box.name_input.edit_finished_value_signal.connect(self.net_manager.update_net_name)

	def build_net(self):
		name = self.net_params_box.name_input.text()
		input_count = self.net_params_box.input_count_input.value()
		layer_sizes = self.layer_params_box.get_layer_sizes()
		neuron_type = self.layer_params_box.default_layer_type_input.selected_type()
		self.net_manager.build_net(name, neuron_type, input_count, layer_sizes)