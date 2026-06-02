import polars as pl

from Graphs.AdjacencyList import AdjacencyList
from algorithms.dijkstra import dijkstra_limitado, reconstruir_camino


def is_oneway(value):
    if value is None:
        return False

    value = str(value).strip().lower()

    return value in ["1", "true", "t", "yes", "y", "si", "sí"]


def clean_distance(value):
    try:
        distance = float(value)
    except:
        return None

    if distance <= 0:
        return None

    if distance != distance:
        return None

    return distance


def read_edges(edges_path):
    edges = pl.read_csv(edges_path)

    required_columns = ["from_id", "to_id", "distance_m", "oneway"]

    for column in required_columns:
        if column not in edges.columns:
            raise ValueError(f"Falta la columna: {column}")

    return edges.select(required_columns)


def get_total_vertices(edges):
    max_from = edges.select(pl.col("from_id").max()).item()
    max_to = edges.select(pl.col("to_id").max()).item()

    return int(max(max_from, max_to)) + 1


def build_graph_from_edges(
    edges_path="datasets/edges.csv",
    representation="adjacency_list",
    edge_limit=None,
):
    if representation != "adjacency_list":
        raise ValueError(
            "Para este módulo se recomienda usar solamente adjacency_list."
        )

    edges = read_edges(edges_path)

    if edge_limit is not None:
        edges = edges.head(edge_limit)

    if edges.height == 0:
        raise ValueError("El archivo edges.csv no tiene datos.")

    total_vertices = get_total_vertices(edges)
    graph = AdjacencyList(total_vertices, directed=True)

    for row in edges.iter_rows(named=True):
        origin = int(row["from_id"])
        destination = int(row["to_id"])
        distance = clean_distance(row["distance_m"])

        if distance is None:
            continue

        graph.add_edge(origin, destination, distance)

        if not is_oneway(row["oneway"]):
            graph.add_edge(destination, origin, distance)

    return graph


def vehicle_reachability(
    graph,
    origin,
    max_distance_m=5000,
    include_origin=False,
):
    distances, parents = dijkstra_limitado(
        graph,
        origin,
        max_distance_m,
    )

    reachable_nodes = len(distances)

    if not include_origin:
        reachable_nodes -= 1

    return {
        "origin": origin,
        "max_distance_m": max_distance_m,
        "reachable_nodes": reachable_nodes,
        "distances": distances,
        "parents": parents,
    }


def print_reachability_summary(
    result,
    show_paths=False,
    limit=20,
):
    origin = result["origin"]
    max_distance_m = result["max_distance_m"]
    reachable_nodes = result["reachable_nodes"]
    distances = result["distances"]
    parents = result["parents"]

    print("\n=== ALCANCE VEHICULAR ===")
    print(f"Nodo origen: {origin}")
    print(f"Distancia máxima: {max_distance_m / 1000:.2f} km")
    print(f"Nodos alcanzables sin contar el origen: {reachable_nodes}")

    nodes = []

    for node, distance in distances.items():
        if node != origin:
            nodes.append((node, distance))

    nodes.sort(key=lambda item: item[1])

    print(f"\nPrimeros {min(limit, len(nodes))} nodos más cercanos:")

    for node, distance in nodes[:limit]:
        if show_paths:
            path = reconstruir_camino(parents, node)
            print(f"Nodo {node} | distancia: {distance:.2f} m | camino: {path}")
        else:
            print(f"Nodo {node} | distancia: {distance:.2f} m")