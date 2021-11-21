from typing import Dict
from pyqtgraph import GraphicsView, GraphicsLayout

from app import NetManager

from .net_plot_data import NetPlotData


class GraphicsWrapper():
	def __init__(self, net_manager: NetManager):
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
		self.cost_graph = self.layout.addPlot(1, 0)
		self.cost_graph.disableAutoRange()
		self.cost_graph.setXLink(self.acc_graph)
		self.cost_graph.showGrid(True, True)

		self.update_interval = 5 # TODO: some way for the user to change this

	def create_plot_data(self, net_id, max_epochs):
		data = NetPlotData(max_epochs)
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