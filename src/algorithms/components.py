from collections import defaultdict
from ..data_structures.union_find import UnionFind


def weak_components(node_ids, from_nodes, to_nodes):
    """Retorna las componentes débiles usando los IDs reales de nodes.csv."""
    id_to_idx = {
        int(node_id): idx
        for idx, node_id in enumerate(node_ids)
    }

    uf = UnionFind(len(node_ids))

    for u, v in zip(from_nodes, to_nodes):
        u = int(u)
        v = int(v)

        if u in id_to_idx and v in id_to_idx:
            uf.union(id_to_idx[u], id_to_idx[v])

    components = defaultdict(list)

    for node_id in node_ids:
        node_id = int(node_id)
        root = uf.find(id_to_idx[node_id])
        components[root].append(node_id)

    return components


def component_stats(node_ids, from_nodes, to_nodes):
    components = weak_components(node_ids, from_nodes, to_nodes)
    sizes = [len(nodes) for nodes in components.values()]

    return {
        "components": components,
        "num_components": len(components),
        "largest_component_size": max(sizes) if sizes else 0,
        "isolated_islands": sum(1 for size in sizes if size == 1),
    }


def largest_component_nodes(node_ids, from_nodes, to_nodes):
    components = weak_components(node_ids, from_nodes, to_nodes)

    if not components:
        return set()

    largest = max(components.values(), key=len)
    return set(largest)