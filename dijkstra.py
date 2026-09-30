"""
Módulo con la implementación del Algoritmo de Dijkstra para rutas de costo mínimo.
Diseñado para uso académico e integración con el proyecto de grafos.
"""


def ejecutar_dijkstra(grafo, id_nodo_origen):
    """Ejecuta el algoritmo de Dijkstra desde un nodo origen determinado.

    Retorna un diccionario con:
    - 'distancias': dict {id_nodo: distancia_minima}
    - 'previos': dict {id_nodo: id_nodo_anterior}
    - 'caminos': dict {id_nodo: [lista_de_nodos_recorrido]}
    - 'aristas_camino': lista de objetos Arista que forman parte de las rutas
    mínimas
    """
    # 1. Validar que no existan pesos negativos
    for arista in grafo.aristas:
        if arista.peso < 0:
            raise ValueError(
                "El algoritmo de Dijkstra no admite aristas con pesos negativos."
            )

    # Buscar el nodo origen
    nodo_origen = grafo.obtener_nodo(id_nodo_origen)
    if not nodo_origen:
        raise ValueError(
            f"El nodo origen con ID '{id_nodo_origen}' no existe en el grafo."
        )

    # 2. Inicialización de estructuras
    distancias = {}
    previos = {}
    no_visitados = []

    for nodo in grafo.nodos:
        distancias[nodo.id] = float("inf")
        previos[nodo.id] = None
        no_visitados.append(nodo.id)

    distancias[nodo_origen.id] = 0

    # 3. Bucle principal de Dijkstra
    while no_visitados:
        # Seleccionar el nodo no visitado con la menor distancia conocida
        nodo_actual_id = min(no_visitados, key=lambda id_n: distancias[id_n])

        # Si el nodo de menor distancia es inalcanzable (distancia inf), terminamos
        if distancias[nodo_actual_id] == float("inf"):
            break

        no_visitados.remove(nodo_actual_id)
        nodo_actual = grafo.obtener_nodo(nodo_actual_id)

        # Evaluar vecinos a través de las aristas incidentes
        for arista in grafo.obtener_aristas_de_nodo(nodo_actual_id):
            # Obtener el nodo vecino al otro extremo de la arista
            vecino_id = (
                arista.nodo2.id
                if arista.nodo1.id == nodo_actual_id
                else arista.nodo1.id
            )

            if vecino_id in no_visitados:
                nueva_distancia = distancias[nodo_actual_id] + arista.peso
                if nueva_distancia < distancias[vecino_id]:
                    distancias[vecino_id] = nueva_distancia
                    previos[vecino_id] = nodo_actual_id

    # 4. Reconstrucción de los caminos (secuencia de nodos)
    caminos = {}
    aristas_camino = []

    for nodo in grafo.nodos:
        dest_id = nodo.id
        if distancias[dest_id] == float("inf"):
            caminos[dest_id] = []  # Inalcanzable
            continue

        # Reconstruir camino desde el destino hacia el origen usando previos
        camino = []
        paso_actual = dest_id
        while paso_actual is not None:
            camino.insert(0, paso_actual)
            paso_actual = previos[paso_actual]

        caminos[dest_id] = camino

        # Identificar las aristas que pertenecen a la ruta mínima
        for i in range(len(camino) - 1):
            u, v = camino[i], camino[i + 1]
            arista_obj = grafo.obtener_arista_entre(u, v)
            if arista_obj and arista_obj not in aristas_camino:
                aristas_camino.append(arista_obj)

    return {
        "distancias": distancias,
        "previos": previos,
        "caminos": caminos,
        "aristas_camino": aristas_camino,
    }