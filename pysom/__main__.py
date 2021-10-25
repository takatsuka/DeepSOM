from graph import som
from graph.graph import Graph



g = Graph()

g.connect(0, 1, 0)
g.set_input([1,2,3])


print(g.get_output())