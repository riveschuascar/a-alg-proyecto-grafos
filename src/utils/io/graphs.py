from ...data_structures.graphs import AdjacencyList, AdjacencyMatrix, EdgeList
import polars as pl
import pickle
import os

def write_pkl(graph, file_name: str) -> None:
    with open(file_name, "wb") as file:
        pickle.dump(graph, file)


def read_pkl(file_name: str) -> AdjacencyList | AdjacencyMatrix | EdgeList:
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"No se encontró el archivo: {file_name}")
    with open(file_name, "rb") as file:
        return pickle.load(file)


def graph_from_csv(type: str, directed: bool = False, weight_col: str = "distance_m") -> AdjacencyList | AdjacencyMatrix | EdgeList:
    nodes = pl.read_csv("datasets/nodes.csv")
    n = nodes["node_id"].n_unique()

    if type == "AdjacencyList":
        g = AdjacencyList(n, directed)
    elif type == "AdjacencyMatrix":
        g = AdjacencyMatrix(n, directed)
    elif type == "EdgeList":
        g = EdgeList(n, directed)
    else:
        raise ValueError(f"Tipo de grafo no soportado: {type}")

    edges = pl.read_csv("datasets/edges-clean.csv")
    edge_rows = edges.select(["from_id", "to_id", weight_col, "oneway"]).rows()

    for from_id, to_id, weight, oneway in edge_rows:
        if directed:
            g.add_edge(from_id, to_id, weight)
            if not oneway:
                g.add_edge(to_id, from_id, weight)
        else:
            g.add_edge(from_id, to_id, weight)

    return g