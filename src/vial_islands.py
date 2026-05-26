import polars as pl
from algorithms import UnionFind

def analyze_weak_components(
    edges_path: str,
    nodes_path: str
):
    print("Leyendo datasets...")

    edges = pl.read_csv(edges_path)
    nodes = pl.read_csv(nodes_path)

    print(f"Nodos: {nodes.height}")
    print(f"Aristas: {edges.height}")

    # IDs reales de nodos
    node_ids = nodes["node_id"].to_list()

    # Mapeo node_id -> índice compacto
    id_to_idx = {
        node_id: idx
        for idx, node_id in enumerate(node_ids)
    }

    n = len(node_ids)

    uf = UnionFind(n)

    print("Procesando aristas...")

    from_nodes = edges["from_id"].to_list()
    to_nodes = edges["to_id"].to_list()

    for u, v in zip(from_nodes, to_nodes):

        if u not in id_to_idx or v not in id_to_idx:
            continue

        uf.union(
            id_to_idx[u],
            id_to_idx[v]
        )

    print("Calculando componentes...")

    components = uf.component_sizes()

    num_components = len(components)

    largest_component_size = max(components.values())

    isolated_islands = sum(
        1 for size in components.values()
        if size == 1
    )

    print("\nRESULTADOS")
    print("-" * 40)

    print(f"Componentes débilmente conexas: {num_components}")

    print(
        f"Tamaño componente principal: "
        f"{largest_component_size}"
    )

    print(f"Total de islas aisladas: {isolated_islands}")

    return {
        "weakly_connected_components": num_components,
        "largest_component_size": largest_component_size,
        "isolated_islands": isolated_islands
    }


if __name__ == "__main__":
    analyze_weak_components(
        edges_path="datasets/edges.csv",
        nodes_path="datasets/nodes.csv"
    )