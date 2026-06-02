import polars as pl

from Graphs.AdjacencyList import AdjacencyList
from algorithms.components import largest_component_nodes
from algorithms.dijkstra import dijkstra_completo, reconstruir_camino
from src.vehicle_range import clean_distance, is_oneway


def read_required_data(edges_path, nodes_path):
    edges = pl.read_csv(edges_path)
    nodes = pl.read_csv(nodes_path)

    edge_columns = ["from_id", "to_id", "distance_m", "oneway"]
    node_columns = ["node_id"]

    for column in edge_columns:
        if column not in edges.columns:
            raise ValueError(f"Falta la columna en edges.csv: {column}")

    for column in node_columns:
        if column not in nodes.columns:
            raise ValueError(f"Falta la columna en nodes.csv: {column}")

    return edges.select(edge_columns), nodes.select(node_columns)


def get_total_vertices_from_nodes(nodes):
    return int(nodes.select(pl.col("node_id").max()).item()) + 1


def build_giant_component_graph(edges, nodes, giant_nodes, respect_oneway=False):
    total_vertices = get_total_vertices_from_nodes(nodes)
    graph = AdjacencyList(total_vertices, directed=True)

    for row in edges.iter_rows(named=True):
        origin = int(row["from_id"])
        destination = int(row["to_id"])

        if origin not in giant_nodes or destination not in giant_nodes:
            continue

        distance = clean_distance(row["distance_m"])

        if distance is None:
            continue

        graph.add_edge(origin, destination, distance)

        if not respect_oneway or not is_oneway(row["oneway"]):
            graph.add_edge(destination, origin, distance)

    return graph


def farthest_node(graph, origin, allowed_nodes):
    distances, parents = dijkstra_completo(
        grafo=graph,
        origen=origin,
        nodos_permitidos=allowed_nodes,
    )

    node, distance = max(
        distances.items(),
        key=lambda item: item[1],
    )

    return node, distance, distances, parents


def road_diameter(
    edges_path="datasets/edges.csv",
    nodes_path="datasets/nodes.csv",
    start_node=None,
    respect_oneway=False,
):
    print("Leyendo datasets...")

    edges, nodes = read_required_data(edges_path, nodes_path)

    node_ids = nodes["node_id"].to_list()
    from_nodes = edges["from_id"].to_list()
    to_nodes = edges["to_id"].to_list()

    print("Buscando componente gigante...")

    giant_nodes = largest_component_nodes(
        node_ids=node_ids,
        from_nodes=from_nodes,
        to_nodes=to_nodes,
    )

    if not giant_nodes:
        raise ValueError("No se encontró componente gigante.")

    if start_node is None or start_node not in giant_nodes:
        start_node = min(giant_nodes)

    print(f"Nodos en componente gigante: {len(giant_nodes)}")
    print("Construyendo grafo de la componente gigante...")

    graph = build_giant_component_graph(
        edges=edges,
        nodes=nodes,
        giant_nodes=giant_nodes,
        respect_oneway=respect_oneway,
    )

    print("Ejecutando Dijkstra 1...")
    node_a, _, _, _ = farthest_node(
        graph=graph,
        origin=start_node,
        allowed_nodes=giant_nodes,
    )

    print("Ejecutando Dijkstra 2...")
    node_b, diameter_m, distances, parents = farthest_node(
        graph=graph,
        origin=node_a,
        allowed_nodes=giant_nodes,
    )

    path = reconstruir_camino(parents, node_b)

    return {
        "node_a": node_a,
        "node_b": node_b,
        "diameter_m": diameter_m,
        "diameter_km": diameter_m / 1000,
        "giant_component_size": len(giant_nodes),
        "path": path,
        "reachable_from_node_a": len(distances),
        "method": "doble Dijkstra sobre componente gigante",
        "respect_oneway": respect_oneway,
    }


def print_diameter_summary(result, show_path=False):
    print("\n=== DIÁMETRO VIAL ===")
    print(f"Método: {result['method']}")
    print(f"Respeta sentido único: {result['respect_oneway']}")
    print(f"Tamaño componente gigante: {result['giant_component_size']}")
    print(f"Intersección A: {result['node_a']}")
    print(f"Intersección B: {result['node_b']}")
    print(f"Mayor distancia mínima: {result['diameter_m']:.2f} m")
    print(f"Mayor distancia mínima: {result['diameter_km']:.2f} km")
    print(f"Nodos alcanzados desde A: {result['reachable_from_node_a']}")

    if show_path:
        print(f"Camino: {result['path']}")


if __name__ == "__main__":
    result = road_diameter()
    print_diameter_summary(result, show_path=False)