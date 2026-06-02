import sys

from src.vehicle_range import (
    build_graph_from_edges,
    vehicle_reachability,
    print_reachability_summary,
)

from src.vial_islands import analyze_weak_components

from src.vial_diameter import road_diameter, print_diameter_summary


def main():
    edges_path = "datasets/edges.csv"
    nodes_path = "datasets/nodes.csv"

    if len(sys.argv) < 2:
        print("Uso:")
        print("python main.py vehicle_range")
        print("python main.py vial_islands")
        print("python main.py diameter")
        return

    option = sys.argv[1]

    if option == "vehicle_range":
        origin = 0
        max_distance_m = 5000
        representation = "adjacency_list"

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

    elif option == "vial_islands":
        analyze_weak_components(
            edges_path=edges_path,
            nodes_path=nodes_path,
        )

    elif option == "diameter":
        result = road_diameter(
            edges_path=edges_path,
            nodes_path=nodes_path,
            start_node=None,
            respect_oneway=False,
        )

        print_diameter_summary(
            result=result,
            show_path=False,
        )

    else:
        print("Opción no válida.")
        print("Opciones:")
        print("- vehicle_range")
        print("- vial_islands")
        print("- diameter")


if __name__ == "__main__":
    main()