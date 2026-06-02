from .graph import Graph

class AdjacencyList(Graph):
    def __init__(self, v: int, directed: bool = False):
        self._adj_list = [[] for _ in range(v)]
        self._vertices = v
        self._is_directed = directed

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self._adj_list[u].append((v, weight))
        if not self._is_directed:
            self._adj_list[v].append((u, weight))

    def remove_edge(self, u: int, v: int) -> None:
        self._adj_list[u].remove((v, self.get_weight(u, v)))
        if not self._is_directed:
            self._adj_list[v].remove((u, self.get_weight(v, u)))

    def has_edge(self, u: int, v: int) -> bool:
        for node in self._adj_list[u]:
            if node[0] == v:
                return True
        return False      
    
    def get_vertices(self) -> int: 
        return self._vertices 

    def get_adj_list(self) -> list[list[tuple[int, int]]]: 
        return self._adj_list 
    
    def neighbors(self, u: int) -> list[int]:
        neighbors = [v for (v, _) in self._adj_list[u]]
        return neighbors

    def transpose(self) -> 'AdjacencyList':
        g = AdjacencyList(self._vertices, directed=True)
        for u in range(self._vertices):
            for (v, w) in self._adj_list[u]:
                g.add_edge(v, u, w)
        return g
    
    def print_graph(self) -> None:
        print("Lista de Adyacencia:")
        for node in range(self._vertices):
            print(node, ": ", end="")
            for (vertex, weight) in self._adj_list[node]:
                print("(", vertex, ",", weight, ") ", end="")
            print() 