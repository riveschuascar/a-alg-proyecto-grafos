from ..data_structures.graphs import Graph, AdjacencyList, AdjacencyMatrix, EdgeList

def kosaraju(graph: Graph) -> list[list[int]]:
    n = graph.get_vertices()
    visited = [False for _ in range(n)]
    stack = []

    for u in range(n):
        if not visited[u]:
            fill_order(graph, u, visited, stack)

    transposed = graph.transpose()

    visited = [False for _ in range(n)]
    sccs = []

    while stack:
        u = stack.pop()
        if not visited[u]:
            scc = []
            dfs_collect(transposed, u, visited, scc)
            sccs.append(scc)

    return sccs

def fill_order(graph: Graph, u: int, visited: list[bool], stack: list[int]) -> None:
    visited[u] = True
    for v in graph.neighbors(u):
        if not visited[v]:
            fill_order(graph, v, visited, stack)
    stack.append(u)

def dfs_collect(transposed: Graph, u: int, visited: list[bool], scc: list) -> None:
    visited[u] = True
    scc.append(u)
    for v in transposed.neighbors(u):
        if not visited[v]:
            dfs_collect(transposed, v, visited, scc)

if __name__ == "__main__":
    """
    Implementacion del algoritmo de Kosaraju para encontrar componentes fuertemente coneectados en un grafo dirigido.
    Se agregaron las funciones `neighbors` y `transpose` a las clases de representacion de los grafos para facilitar la implementación de un algoritmo generico.
    Para la ejecucion:
    - Se debe ejecutar el archivo `kosaraju.py` y no los archivos de las representaciones de grafos.
    - Verificar que la estructura de los modulos y archivos sea:
        Graphs/
            __init__.py
            Graph.py
            AdjacencyList.py
            AdjacencyMatrix.py
            EdgeList.py
        kosaraju.py
    - Se probo con la version de python 3.13.0
    """
    for GraphClass in [AdjacencyList, AdjacencyMatrix, EdgeList]:
        g = GraphClass(v=6, directed=True)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        g.add_edge(4, 3)
        g.add_edge(5, 0)
        g.add_edge(4, 1)

        result = kosaraju(g)
        print(f"{GraphClass.__name__}: {result}")