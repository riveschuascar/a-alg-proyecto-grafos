import heapq


def dijkstra_limitado(grafo, origen, distancia_maxima):
    if origen < 0 or origen >= grafo.get_vertices():
        raise ValueError("El nodo origen no existe en el grafo.")

    lista_adyacencia = grafo.get_adj_list()

    distancias = {origen: 0}
    padres = {origen: None}
    cola = [(0, origen)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in lista_adyacencia[nodo_actual]:
            nueva_distancia = distancia_actual + float(peso)

            if nueva_distancia > distancia_maxima:
                continue

            if nueva_distancia < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, padres

def dijkstra_completo(grafo, origen, nodos_permitidos=None):
    if origen < 0 or origen >= grafo.get_vertices():
        raise ValueError("El nodo origen no existe en el grafo.")

    lista_adyacencia = grafo.get_adj_list()

    distancias = {origen: 0}
    padres = {origen: None}
    cola = [(0, origen)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in lista_adyacencia[nodo_actual]:
            if nodos_permitidos is not None and vecino not in nodos_permitidos:
                continue

            nueva_distancia = distancia_actual + float(peso)

            if nueva_distancia < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, padres


def reconstruir_camino(padres, destino):
    if destino not in padres:
        return []

    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = padres[actual]

    camino.reverse()
    return camino