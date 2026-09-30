class UnionFind:
    def __init__(self, nodos):
        self.padre = {u: u for u in nodos}

    def find(self, u):
        if self.padre[u] == u:
            return u
        self.padre[u] = self.find(self.padre[u])
        return self.padre[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.padre[root_u] = root_v
            return True
        return False

    def clone(self):
        nuevo_uf = UnionFind([])
        nuevo_uf.padre = self.padre.copy()
        return nuevo_uf


def ejecutar_kruskal(nodos, arcos):
    """
    Ejecuta el algoritmo de Kruskal clasificando formalmente las aristas en:
    1. AEM (Seleccionadas): Forman el Árbol de Expansión Mínima.
    2. Alternativas por empate: Aristas con el mismo peso que una arista seleccionada
       que NO formaban ciclo en su momento (unían componentes conexas distintas),
       pero quedaron fuera por la elección de otra arista del mismo grupo de peso.
    3. Ciclos (Descartadas): Aristas que conectan nodos que YA estaban conectados
       previamente en la estructura de bosques.
    """
    if not nodos or not arcos:
        return {
            "aem": [],
            "alternativos": [],
            "ciclos": [],
            "peso_total": 0.0,
            "historial": []
        }

    # 1. Agrupar aristas por peso
    arcos_ordenados = sorted(arcos, key=lambda x: x[2])
    grupos_por_peso = {}
    for u, v, w in arcos_ordenados:
        grupos_por_peso.setdefault(w, []).append((u, v, w))

    uf = UnionFind(nodos)

    arcos_aem = []
    arcos_alternativos = []
    arcos_ciclos = []
    historial_pasos = []
    peso_total = 0.0
    paso_num = 1

    # 2. Procesar grupo a grupo de peso
    for peso, grupo_arcos in grupos_por_peso.items():
        # Si sólo hay una arista con este peso, la evaluación es estándar
        if len(grupo_arcos) == 1:
            u, v, w = grupo_arcos[0]
            if uf.union(u, v):
                arcos_aem.append((u, v, w))
                peso_total += w
                historial_pasos.append(
                    f"Paso {paso_num}: Arco ({u} - {v}) [Peso: {w}] -> ACEPTADO (Sin ciclo)"
                )
            else:
                arcos_ciclos.append((u, v, w))
                historial_pasos.append(
                    f"Paso {paso_num}: Arco ({u} - {v}) [Peso: {w}] -> RECHAZADO (Genera ciclo)"
                )
            paso_num += 1
        else:
            # Hay EMPATE de pesos. Analizamos qué aristas son válidas ANTES de modificar el UnionFind.
            uf_estado_inicial_grupo = uf.clone()

            # Determinamos cuáles de las aristas con empatado peso forman ciclo desde el principio
            es_ciclo_inicial = {}
            for u, v, w in grupo_arcos:
                # Si en el estado previo al grupo ya están conectados -> es ciclo directo
                if uf_estado_inicial_grupo.find(u) == uf_estado_inicial_grupo.find(v):
                    es_ciclo_inicial[(u, v, w)] = True
                else:
                    es_ciclo_inicial[(u, v, w)] = False

            # Ahora procesamos el grupo en Kruskal normal
            seleccionados_en_grupo = []
            for u, v, w in grupo_arcos:
                if es_ciclo_inicial[(u, v, w)]:
                    arcos_ciclos.append((u, v, w))
                    historial_pasos.append(
                        f"Paso {paso_num}: Arco ({u} - {v}) [Peso: {w}] -> RECHAZADO (Genera ciclo)"
                    )
                else:
                    # No era ciclo al inicio del grupo
                    if uf.union(u, v):
                        arcos_aem.append((u, v, w))
                        seleccionados_en_grupo.append((u, v, w))
                        peso_total += w
                        historial_pasos.append(
                            f"Paso {paso_num}: Arco ({u} - {v}) [Peso: {w}] -> ACEPTADO (Sin ciclo)"
                        )
                    else:
                        # No era ciclo al inicio del grupo, pero al aplicar otra arista de igual peso
                        # de este grupo, pasó a formar un ciclo. ¡Esta es una ALTERNATIVA por empate!
                        arcos_alternativos.append((u, v, w))
                        historial_pasos.append(
                            f"Paso {paso_num}: Arco ({u} - {v}) [Peso: {w}] -> ALTERNATIVA POR EMPATE (No seleccionada)"
                        )
                paso_num += 1

    return {
        "aem": arcos_aem,
        "alternativos": arcos_alternativos,
        "ciclos": arcos_ciclos,
        "peso_total": peso_total,
        "historial": historial_pasos
    }