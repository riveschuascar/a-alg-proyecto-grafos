from .data_structures.graphs import AdjacencyList
from .data_structures.union_find import UnionFind

def analyze_weak_components(graph: AdjacencyList):
    n = graph.get_vertices()
    uf = UnionFind(n)

    print(f"Nodos: {n}")
    print("Procesando aristas...")

    for u, neighbors in enumerate(graph.get_adj_list()):
        for v, _ in neighbors:
            uf.union(u, v)

    print("Calculando componentes...")

    components = uf.component_sizes()
    num_components = len(components)
    largest_component_size = max(components.values())
    isolated_islands = sum(1 for size in components.values() if size == 1)

    print("\nRESULTADOS")
    print("-" * 40)
    print(f"Componentes débilmente conexas: {num_components}")
    print(f"Tamaño componente principal: {largest_component_size}")
    print(f"Total de islas aisladas: {isolated_islands}")

    largest_component_root = max(components, key=components.get)
    giant_nodes = {
        idx for idx in range(n)
        if uf.find(idx) == largest_component_root
    }
    return {
        "weakly_connected_components": num_components,
        "largest_component_size": largest_component_size,
        "isolated_islands": isolated_islands,
        "giant_nodes": giant_nodes
    }