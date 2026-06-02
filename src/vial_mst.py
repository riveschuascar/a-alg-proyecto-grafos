from .data_structures.graphs import AdjacencyList
from .algorithms.mst import kruskal

def find_mst_gig_component(graph: AdjacencyList, giant_nodes: set):
    mst_edges, total_km = kruskal(graph, giant_nodes)
    print("\nMST - RED DE EMERGENCIA MÍNIMA")
    print("-" * 40)
    print(f"Aristas en MST:     {len(mst_edges)}")
    print(f"Nodos cubiertos:    {len(giant_nodes)}")
    print(f"Distancia total:    {total_km:.2f} km")