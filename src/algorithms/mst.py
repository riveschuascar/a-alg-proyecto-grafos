from ..data_structures.graphs import AdjacencyList
from ..data_structures.union_find import UnionFind

def kruskal(graph: AdjacencyList, giant_nodes: set) -> tuple[list, float]:
    edges = [
        (w, u, v)
        for u, neighbors in enumerate(graph.get_adj_list())
        for v, w in neighbors
        if u in giant_nodes and v in giant_nodes and u < v
    ]

    edges.sort()

    uf = UnionFind(graph.get_vertices())
    mst_edges = []
    total_distance = 0.0

    for w, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v, w))
            total_distance += w

    total_km = total_distance / 1000

    return mst_edges, total_km