from __future__ import annotations
from numpy import array, moveaxis, concatenate
from pysom.node import Node
from pysom.graph import Graph
from pysom.nodes.som import SOM
from pysom.nodes.bmu import BMU
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
import multiprocessing

from ..deprecated import deprecated

import warnings
warnings.warn(f"""Module {__name__} have never been tested and was deprecated. 
                  Any usages is not recommend and the behavior is undefined""",
              DeprecationWarning, stacklevel=2)

BMU_1D = "1D"
BMU_2D = "2D"


class Layer(Node):
    """
    Node type for holding many SOMs at once.
    The SOMs follow the same rules and structure as the graph's independent
    SOM node. The advantage of this node is that it makes the independence of
    parallel SOMs explicit, and can feed data through several SOMs
    simultaneously. Multiprocessing may optionally be used in the evaluating
    of the layer. It may also be easier to set up than a full graph structure
    for several parallel SOMs.

    Args:
        uid (str): the unique integer ID of the Layer node instance
        graph (Graph): the containing Graph instance holding the \
            constructed Layer node
        parallel_mode (bool): whether the Layer will spawn additional
            processes to perform evaluation on the different SOMs in parallel.
        all_som_props (list): a list of dictionaries. Each dictionary should
            contain the attributes desired to build one SOM, with arguments
            the same as when constructing a SOM node in the graph. The Layer
            will be formed from the resulting SOMs, in the given order
        bmu_output (str): As in the BMU Node class. Determines whether the
            bmu nodes extracting output from the SOMs inside the layer
            will output in 1D or 2D mode. Must be either "1D" or "2D".
            Defaults to 2D
    """
    @deprecated
    def __init__(self, uid: int, graph, parallel_mode: bool,
                 all_som_props: list, bmu_output: str = "2D"):

        super(Layer, self).__init__(uid, graph)

        self.layer_graph = Graph()
        self.parallel_mode = parallel_mode
        self.bmu_output = bmu_output

        som_count = len(all_som_props)

        layer_inlen = 0
        som_inlens = []
        all_soms = []
        all_bmus = []
        selections = []

        for som_info in all_som_props:

            new_som = self.layer_graph.create(node_type=SOM, props=som_info)
            all_soms.append(new_som)

            dim = som_info["dim"]
            som_inlens.append(dim)

            som_input = (1, list(range(layer_inlen, layer_inlen + dim)))
            selections.append(som_input)
            layer_inlen += dim

            new_bmu = self.layer_graph.create(
                node_type=BMU, props={"output": bmu_output})
            all_bmus.append(new_bmu)

            self.layer_graph.connect(new_som, new_bmu, 0)

        dist = self.layer_graph.create(Dist, {"selections": selections})
        conc = self.layer_graph.create(Concat, {"axis": 1})

        for i in range(len(all_soms)):
            curr_som = all_soms[i]
            curr_bmu = all_bmus[i]
            self.layer_graph.connect(dist, curr_som, i + 1)
            self.layer_graph.connect(curr_bmu, conc, 1)

        self.layer_graph.connect(self.layer_graph.start, dist, 1)
        self.layer_graph.connect(conc, self.layer_graph.end, 1)

        self.som_count = som_count
        self.conc = self.layer_graph.find_node(conc)

    @deprecated
    def __str__(self) -> str:
        str_rep = "LayerNode {}".format(self.uid)
        return str_rep

    @deprecated
    def process_route(self, i, q):
        result = self.conc.get_input(index=i)
        q.put((i, result))

    @deprecated
    def _evaluate(self):

        self.layer_graph.set_input(self.get_input())

        all_bmu_outs = [None for _ in range(self.som_count)]

        if self.parallel_mode:

            process_list = []

            return_queue = multiprocessing.Queue()

            for i in range(self.som_count):
                p = multiprocessing.Process(
                    target=self.process_route,
                    args=(i, return_queue))
                process_list.append(p)
                p.start()

            returned_processes = 0
            while returned_processes < self.som_count:
                val = return_queue.get()
                all_bmu_outs[val[0]] = val[1]
                process_list[val[0]].join()
                returned_processes += 1

        else:
            for i in range(self.som_count):
                all_bmu_outs[i] = self.conc.get_input(index=i)

        self.conc.precon = concatenate(all_bmu_outs, -1)

        self.conc.output_ready = True
        self.output_ready = True

    @deprecated
    def get_output(self, slot: int):
        if not self.output_ready:
            self._evaluate()

        return self.layer_graph.get_output()

    @deprecated
    def check_slot(self, slot: int) -> bool:
        if (slot != 1):
            raise RuntimeError("Layer Node only accepts connections on slot 1")
        return True


if __name__ == "__main__":
    pass
