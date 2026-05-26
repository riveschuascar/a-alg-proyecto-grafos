from .Graph import Graph

class AdjacencyMatrix(Graph):
    def __init__(self, v: int, directed: bool = False):
        self._adj_matrix = [[0 for _ in range(v)] for _ in range(v)]
        self._vertices = v
        self._is_directed = directed

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self._adj_matrix[u][v] = weight
        if not self._is_directed:
            self._adj_matrix[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        self._adj_matrix[u][v] = 0
        if not self._is_directed:
            self._adj_matrix[v][u] = 0

    def has_edge(self, u: int, v: int) -> bool:
        return self._adj_matrix[u][v] != 0

    def get_vertices(self) -> int:
        return self._vertices

    def get_adj_matrix(self) -> list[list[int]]:
        return self._adj_matrix
    
    def neighbors(self, u: int) -> list[int]:
        neighbors = [v for v in range(self._vertices) if self._adj_matrix[u][v] != 0]
        return neighbors

    def transpose(self) -> 'AdjacencyMatrix':
        g = AdjacencyMatrix(self._vertices, directed=True)
        for u in range(self._vertices):
            for v in range(self._vertices):
                if self._adj_matrix[u][v] != 0:
                    g.add_edge(v, u, self._adj_matrix[u][v])
        return g
    
    def print_graph(self) -> None:
        print("Matriz de Adyacencia:")
        for i in range(self._vertices):
            for j in range(self._vertices):
                print(self._adj_matrix[i][j], end=" ")
            print()