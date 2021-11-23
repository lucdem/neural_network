from typing import Dict
from random import randint

from pyqtgraph import GraphicsView, GraphicsLayout
import pyqtgraph

from app import NetManager

from .net_plot_data import NetPlotData


_line_colors = [
	(250, 128, 114),
	(255, 69, 0),
	(255, 140, 0),
	(255, 215, 0),
	(154, 205, 50),
	(0, 255, 0),
	(0, 250, 154),
	(102, 205, 170),
	(32, 178, 170),
	(0, 255, 255),
	(135, 206, 235),
	(0, 0, 255),
	(138, 43, 226),
	(255, 0, 255),
	(255, 20, 147),
	(255, 228, 196),
	(244, 164, 96),
	(255, 255, 255),
	(169, 169, 169)
]


def _random_color():
	return _line_colors[randint(0, len(_line_colors) - 1)]


_line_width = 1 # TODO: some way for the user to change this


class GraphicsWrapper():
	def __init__(self, net_manager: NetManager):
		pyqtgraph.setConfigOptions(antialias = True)

		self.widget = GraphicsView()
		self.layout = GraphicsLayout()
		self.widget.setCentralItem(self.layout)

		self.net_manager = net_manager
		self.net_graph_data_dict: Dict[int, NetPlotData] = {}

		self.acc_graph = self.layout.addPlot(0, 0)
		self.acc_graph.disableAutoRange()
		self.acc_graph.getAxis('bottom').setStyle(showValues=False)
		self.acc_graph.showGrid(True, True)
		self.acc_graph.setYRange(0, 100)
		self.acc_graph.addLegend(offset = (5, 5))

		self.cost_graph = self.layout.addPlot(1, 0)
		self.cost_graph.disableAutoRange()
		self.cost_graph.setXLink(self.acc_graph)
		self.cost_graph.showGrid(True, True)
		self.cost_graph.addLegend(offset = (-5, 5))

		self.update_interval = 5 # TODO: some way for the user to change this

	def create_plot_data(self, net_id, max_epochs):
		data = self.net_graph_data_dict.get(net_id)
		if data is not None:
			self.cost_graph.removeItem(data.cost_data_item)
			self.acc_graph.removeItem(data.acc_data_item)
			pen_params = data.pen_params
		else:
			pen_params = self.create_pen_params()
		data = NetPlotData(max_epochs, self.net_manager.net_by_id[net_id].name, pen_params)
		self.net_graph_data_dict[net_id] = data
		self.cost_graph.addDataItem(data.cost_data_item)
		self.acc_graph.addDataItem(data.acc_data_item)

	def update_graphs(self, net_id, epoch, cost, acc):
		data = self.net_graph_data_dict[net_id]
		data.add_point(epoch, cost, acc)

		if epoch % self.update_interval == 0 or epoch == data.acc.size:
			self.cost_graph.setXRange(0, data.cost.size)
			self.cost_graph.setYRange(0, data.max_cost)
			data.refresh()

	def create_pen_params(self):
		return {'color': _random_color(), 'width': _line_width}