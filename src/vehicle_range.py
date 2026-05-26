from __future__ import annotations

import heapq
import math
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable

import polars as pl

from graphs import AdjacencyMatrix, AdjacencyList, EdgeList

WeightedNeighbor = tuple[int, float]

def _is_oneway(value) -> bool:
    """
    Convierte el valor de la columna oneway a booleano.

    En el dataset puede venir como 1/0, true/false, yes/no, T/F, etc.
    True  -> la calle solo se recorre de from_id hacia to_id.
    False -> la calle se recorre en ambos sentidos.
    """
    if value is None:
        return False

    text = str(value).strip().lower()
    return text in {"1", "true", "t", "yes", "y", "si", "sí"}


def _safe_distance(value) -> float | None:
    """
    Convierte distance_m a float y descarta valores inválidos.
    """
    try:
        distance = float(value)
    except (TypeError, ValueError):
        return None

    if math.isnan(distance) or distance <= 0:
        return None

    return distance


def build_graph_from_edges(
    edges_path: str | Path = "datasets/edges.csv",
    representation: str = "adjacency_list",
    edge_limit: int | None = None,
):
    """
    Construye el grafo vial desde datasets/edges.csv usando Polars.

    Columnas esperadas:
    - from_id
    - to_id
    - distance_m
    - oneway

    representation puede ser:
    - adjacency_list
    - adjacency_matrix
    - edge_list
    """
    edges_path = Path(edges_path)

    if not edges_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {edges_path}")

    df = pl.read_csv(edges_path)

    required_columns = {"from_id", "to_id", "distance_m", "oneway"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Faltan columnas en edges.csv: {missing_columns}")

    if edge_limit is not None:
        df = df.head(edge_limit)

    if df.height == 0:
        raise ValueError("edges.csv no tiene aristas para construir el grafo.")

    max_from = df.select(pl.col("from_id").max()).item()
    max_to = df.select(pl.col("to_id").max()).item()
    vertices = int(max(max_from, max_to)) + 1

    representation = representation.lower().strip()

    if representation == "adjacency_list":
        graph = AdjacencyList(vertices, directed=True)

    elif representation == "adjacency_matrix":
        graph = AdjacencyMatrix(vertices, directed=True)

    elif representation == "edge_list":
        graph = EdgeList(vertices, directed=True)

    else:
        raise ValueError(
            "Representación inválida. Usa: adjacency_list, adjacency_matrix o edge_list."
        )

    for row in df.select(["from_id", "to_id", "distance_m", "oneway"]).iter_rows(named=True):
        u = int(row["from_id"])
        v = int(row["to_id"])
        distance = _safe_distance(row["distance_m"])

        if distance is None:
            continue

        # Sentido original de la arista.
        graph.add_edge(u, v, distance)

        # Si la calle NO es de un solo sentido, se agrega también el regreso.
        if not _is_oneway(row["oneway"]):
            graph.add_edge(v, u, distance)

    return graph


def _neighbors_from_adjacency_list(
    graph: AdjacencyList,
) -> Callable[[int], Iterable[WeightedNeighbor]]:
    adj = graph.get_adj_list()

    def get_neighbors(u: int) -> Iterable[WeightedNeighbor]:
        return adj[u]

    return get_neighbors


def _neighbors_from_adjacency_matrix(
    graph: AdjacencyMatrix,
) -> Callable[[int], Iterable[WeightedNeighbor]]:
    matrix = graph.get_adj_matrix()

    def get_neighbors(u: int) -> Iterable[WeightedNeighbor]:
        row = matrix[u]

        for v, weight in enumerate(row):
            if weight != 0:
                yield v, float(weight)

    return get_neighbors


def _neighbors_from_edge_list(
    graph: EdgeList,
) -> Callable[[int], Iterable[WeightedNeighbor]]:
    """
    La lista de aristas no permite consultar vecinos rápido directamente.
    Por eso se crea un índice auxiliar:

    nodo -> [(vecino, peso), ...]

    Sigue partiendo de la representación EdgeList, pero evita recorrer todas
    las aristas cada vez que se visita un nodo.
    """
    index = defaultdict(list)

    for edge in graph.get_edge_list():
        index[edge.u].append((edge.v, float(edge.weight)))

    def get_neighbors(u: int) -> Iterable[WeightedNeighbor]:
        return index[u]

    return get_neighbors


def _get_weighted_neighbors_function(
    graph,
) -> Callable[[int], Iterable[WeightedNeighbor]]:
    """
    Detecta qué representación de grafo se está usando y devuelve una función
    para obtener vecinos con peso.
    """
    if isinstance(graph, AdjacencyList):
        return _neighbors_from_adjacency_list(graph)

    if isinstance(graph, AdjacencyMatrix):
        return _neighbors_from_adjacency_matrix(graph)

    if isinstance(graph, EdgeList):
        return _neighbors_from_edge_list(graph)

    raise TypeError("Tipo de grafo no soportado para alcance vehicular.")


def vehicle_reachability(
    graph,
    origin: int,
    max_distance_m: float = 5000.0,
    include_origin: bool = False,
) -> dict:
    """
    Calcula cuántos nodos son alcanzables desde origin usando máximo max_distance_m.

    Como las calles tienen pesos en metros, se usa Dijkstra acotado por distancia.
    No se usa distancia euclidiana.

    Retorna:
    - origin: nodo origen
    - max_distance_m: distancia máxima permitida
    - count: cantidad de nodos alcanzables
    - distances: distancia mínima desde origin hacia cada nodo alcanzable
    - parents: padre de cada nodo para reconstruir el camino mínimo
    """
    if origin < 0 or origin >= graph.get_vertices():
        raise ValueError(
            f"El nodo origen {origin} no existe. "
            f"El grafo tiene nodos desde 0 hasta {graph.get_vertices() - 1}."
        )

    get_neighbors = _get_weighted_neighbors_function(graph)

    distances: dict[int, float] = {origin: 0.0}
    parents: dict[int, int | None] = {origin: None}
    priority_queue: list[tuple[float, int]] = [(0.0, origin)]

    while priority_queue:
        current_distance, u = heapq.heappop(priority_queue)

        # Si esta distancia ya fue superada por una mejor, se ignora.
        if current_distance > distances[u]:
            continue

        for v, weight in get_neighbors(u):
            new_distance = current_distance + float(weight)

            # Poda: si pasa de 5 km, ese camino ya no sirve.
            if new_distance > max_distance_m:
                continue

            if new_distance < distances.get(v, math.inf):
                distances[v] = new_distance
                parents[v] = u
                heapq.heappush(priority_queue, (new_distance, v))

    count = len(distances) if include_origin else len(distances) - 1

    return {
        "origin": origin,
        "max_distance_m": max_distance_m,
        "count": count,
        "distances": distances,
        "parents": parents,
    }


def reconstruct_path(parents: dict[int, int | None], target: int) -> list[int]:
    """
    Reconstruye el camino mínimo desde el origen hasta target.
    """
    if target not in parents:
        return []

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def print_reachability_summary(
    result: dict,
    show_paths: bool = False,
    limit: int = 20,
) -> None:
    """
    Imprime un resumen del alcance vehicular.
    """
    origin = result["origin"]
    max_distance_m = result["max_distance_m"]
    count = result["count"]
    distances = result["distances"]
    parents = result["parents"]

    print("\n=== ALCANCE VEHICULAR ===")
    print(f"Nodo origen: {origin}")
    print(f"Distancia máxima: {max_distance_m / 1000:.2f} km")
    print(f"Nodos alcanzables sin contar el origen: {count}")

    reachable_nodes = [
        (node, distance)
        for node, distance in distances.items()
        if node != origin
    ]

    reachable_nodes.sort(key=lambda item: item[1])

    print(f"\nPrimeros {min(limit, len(reachable_nodes))} nodos más cercanos:")

    for node, distance in reachable_nodes[:limit]:
        if show_paths:
            path = reconstruct_path(parents, node)
            print(f"Nodo {node} | distancia: {distance:.2f} m | camino: {path}")
        else:
            print(f"Nodo {node} | distancia: {distance:.2f} m")