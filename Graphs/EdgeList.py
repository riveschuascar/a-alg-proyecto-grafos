from .Graph import Graph

class Edge:
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight

class EdgeList(Graph):
    def __init__(self, v: int, directed: bool = False):
        self._edges = []
        self._vertices = v
        self._is_directed = directed

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self._edges.append(Edge(u, v, weight))
        if not self._is_directed:
            self._edges.append(Edge(v, u, weight))

    def print_graph(self) -> None:
        print("Lista de Aristas:")
        for e in self._edges:
            print(f"{e.u} -> {e.v} (peso: {e.weight})")

    def get_vertices(self) -> int:
        return self._vertices
    
    def get_edge_list(self) -> list[Edge]:
        return self._edges
    
    def neighbors(self, u: int) -> list[int]:
        neighbors = [e.v for e in self._edges if e.u == u]
        return neighbors

    def transpose(self) -> 'EdgeList':
        g = EdgeList(self._vertices, directed=True)
        for e in self._edges:
            g.add_edge(e.v, e.u, e.weight)
        return g