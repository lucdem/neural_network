from pyqtgraph import GraphicsView, GraphicsLayout


class GraphWrapper():
	def __init__(self):
		self.widget = GraphicsView()
		self.layout = GraphicsLayout()
		self.widget.setCentralItem(self.layout)

		self.acc_graph = self.layout.addPlot(0, 0)
		self.acc_graph.getAxis('bottom').setStyle(showValues=False)
		self.acc_graph.showGrid(True, True)
		self.cost_graph = self.layout.addPlot(1, 0)
		self.cost_graph.setXLink(self.acc_graph)
		self.cost_graph.showGrid(True, True)

		pass