#Representa las ubicaciones y sus distancias mediante un grafo y utiliza Dijkstra para encontrar un camino de menor distancia.
import heapq
#Distancias simuladas en kilómetros entre ubicaciones de Ibagué
grafo = {
    "Centro": {
        "La Estacion": 2,
        "Universidad del Tolima": 5
    },
    "La Estacion": {
        "Centro": 2,
        "Picaleña": 7
    },
    "Universidad del Tolima": {
        "Centro": 5,
        "Picaleña": 6
    },
    "Picaleña": {
        "La Estacion": 7,
        "Universidad del Tolima": 6
    }
}
def dijkstra(origen, destino):
    if origen not in grafo or destino not in grafo:
        return None, float("inf")
    distancias = {punto: float("inf") for punto in grafo}
    anteriores = {punto: None for punto in grafo}
    distancias[origen] = 0
    pendientes = [(0, origen)]
    while pendientes:
        distancia_actual, actual = heapq.heappop(pendientes)
        if distancia_actual > distancias[actual]:
            continue
        if actual == destino:
            break
        for vecino, distancia in grafo[actual].items():
            nueva_distancia = distancia_actual + distancia
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = actual
                heapq.heappush(pendientes, (nueva_distancia, vecino))
    if distancias[destino] == float("inf"):
        return None, float("inf")
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = anteriores[actual]
    camino.reverse()
    return camino, distancias[destino]