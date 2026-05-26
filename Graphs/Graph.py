from abc import ABC, abstractmethod

class Graph(ABC):
    @abstractmethod
    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """
        Adds an edge from vertex u to vertex v with the given weight
        If the graph is undirected, also adds an edge from v to u
        """
        pass

    @abstractmethod
    def get_vertices(self) -> int:
        """"Returns the number of nodes in the graph"""
        pass

    @abstractmethod
    def neighbors(self, u: int) -> list[int]:
        """Returns a list of neighbors for vertex u"""
        pass

    @abstractmethod
    def transpose(self) -> 'Graph':
        """Returns a new graph with all edges inverted"""
        pass
