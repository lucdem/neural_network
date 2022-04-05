import numpy
from pyqtgraph import PlotDataItem


class NetPlotData:
	def __init__(self, max_epochs, legend_label, pen_params) -> None:
		self.epochs = numpy.array(range(0, max_epochs))
		self.cost = numpy.array([-10.0] * max_epochs)
		self.max_cost = 0
		self.acc = numpy.array([-10.0] * max_epochs)

		self.pen_params = pen_params

		self.cost_data_item = PlotDataItem(self.epochs, self.cost, name = legend_label)
		self.cost_data_item.setPen(self.pen_params)
		self.acc_data_item = PlotDataItem(self.epochs, self.acc, name = legend_label)
		self.acc_data_item.setPen(self.pen_params)

	def update_pen(self, line_width: int):
		self.pen_params['width'] = line_width
		self.cost_data_item.setPen(self.pen_params)
		self.acc_data_item.setPen(self.pen_params)

	def add_point(self, epoch, cost, acc):
		self.cost[epoch] = cost
		if cost > self.max_cost:
			self.max_cost = cost
		self.acc[epoch] = acc

	def refresh(self):
		self.cost_data_item.setData(self.epochs, self.cost)
		self.acc_data_item.setData(self.epochs, self.acc)