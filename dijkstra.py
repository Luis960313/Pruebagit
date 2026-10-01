"""
Módulo con la implementación del Algoritmo de Dijkstra para rutas de costo mínimo.
"""

def ejecutar_dijkstra(grafo, nodo_origen):
    # Validar pesos negativos
    for u, v, w in grafo.arcos:
        if w < 0:
            raise ValueError("El algoritmo de Dijkstra no admite arcos con pesos negativos.")

    if nodo_origen not in grafo.nodos:
        raise ValueError(f"El nodo origen '{nodo_origen}' no existe en el grafo.")

    # Inicialización
    distancias = {nodo: float('inf') for nodo in grafo.nodos}
    previos = {nodo: None for nodo in grafo.nodos}
    distancias[nodo_origen] = 0

    no_visitados = list(grafo.nodos.keys())

    # Construir lista de adyacencia
    adyacencia = {nodo: [] for nodo in grafo.nodos}
    for u, v, w in grafo.arcos:
        adyacencia[u].append((v, w))
        adyacencia[v].append((u, w))  # Grafo no dirigido

    while no_visitados:
        # Seleccionar nodo no visitado con menor distancia
        nodo_actual = min(no_visitados, key=lambda n: distancias[n])

        if distancias[nodo_actual] == float('inf'):
            break

        no_visitados.remove(nodo_actual)

        # Evaluar vecinos
        for vecino, peso in adyacencia[nodo_actual]:
            if vecino in no_visitados:
                nueva_dist = distancias[nodo_actual] + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    previos[vecino] = nodo_actual

    # Reconstruir caminos y arcos utilizados
    caminos = {}
    caminos_arcos = []

    for nodo in grafo.nodos:
        if distancias[nodo] == float('inf'):
            caminos[nodo] = []
            continue

        camino = []
        actual = nodo
        while actual is not None:
            camino.insert(0, actual)
            actual = previos[actual]

        caminos[nodo] = camino

        # Registrar los arcos pertenecientes al camino mínimo
        for i in range(len(camino) - 1):
            u_c, v_c = camino[i], camino[i + 1]
            if (u_c, v_c) not in caminos_arcos and (v_c, u_c) not in caminos_arcos:
                caminos_arcos.append((u_c, v_c))

    return {
        "origen": nodo_origen,
        "distancias": distancias,
        "caminos": caminos,
        "caminos_arcos": caminos_arcos
    }