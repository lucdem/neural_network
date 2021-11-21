import numpy
from pyqtgraph import PlotDataItem


class NetPlotData:
	def __init__(self, max_epochs, plot_interval = 1) -> None:
		size = max_epochs // plot_interval
		self.epochs = numpy.array(range(0, max_epochs, plot_interval))
		self.cost = numpy.array([-10.0] * size)
		self.max_cost = 0
		self.acc = numpy.array([-10.0] * size)
		self.cost_data_item = PlotDataItem(self.epochs, self.cost)
		self.acc_data_item = PlotDataItem(self.epochs, self.acc)

	def add_point(self, epoch, cost, acc):
		self.cost[epoch] = cost
		if cost > self.max_cost:
			self.max_cost = cost
		self.acc[epoch] = acc

	def refresh(self):
		self.cost_data_item.setData(self.epochs, self.cost)
		self.acc_data_item.setData(self.epochs, self.acc)