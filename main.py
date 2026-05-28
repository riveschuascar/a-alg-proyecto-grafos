from src.vehicle_range import (
    build_graph_from_edges,
    vehicle_reachability,
    print_reachability_summary,
)

from src.vial_islands import analyze_weak_components


def main():
    # Nodo origen
    origin = 0

    # Distancia máxima: 5 km = 5000 metros
    max_distance_m = 5000

    # Representación del grafo
    representation = "adjacency_list"

    # Datasets
    edges_path = "datasets/edges.csv"
    nodes_path = "datasets/nodes.csv"

    print("Construyendo grafo...")

    graph = build_graph_from_edges(
        edges_path=edges_path,
        representation=representation,
    )

    print("Calculando alcance vehicular...")

    result = vehicle_reachability(
        graph=graph,
        origin=origin,
        max_distance_m=max_distance_m,
        include_origin=False,
    )

    print_reachability_summary(
        result=result,
        show_paths=False,
        limit=20,
    )

    analyze_weak_components(
        edges_path=edges_path,
        nodes_path=nodes_path,
    )


if __name__ == "__main__":
    main()