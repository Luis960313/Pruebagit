def redibujar_grafo(canvas, grafo, resultado_aem=None, nodo_seleccionado=None,
                    arco_evaluando=None, estado_evaluacion=None, solo_aem=False,
                    resultado_dijkstra=None, nodo_origen_dijkstra=None):
    canvas.delete("all")

    # Datos AEM (Kruskal)
    arcos_aem = resultado_aem["aem"] if resultado_aem else []
    arcos_alt = resultado_aem["alternativos"] if resultado_aem else []
    arcos_cic = resultado_aem["ciclos"] if resultado_aem else []
    peso_total = resultado_aem["peso_total"] if resultado_aem else 0.0

    # Datos Dijkstra
    arcos_dijkstra = resultado_dijkstra["caminos_arcos"] if resultado_dijkstra else []
    distancias_dijkstra = resultado_dijkstra["distancias"] if resultado_dijkstra else {}
    origen_dijkstra = resultado_dijkstra["origen"] if resultado_dijkstra else nodo_origen_dijkstra

    # 1. Dibujar Arcos
    for u, v, w in grafo.arcos:
        es_aem = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_aem)
        es_alt = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_alt)
        es_cic = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_cic)

        # Identificar si el arco pertenece a la ruta mínima de Dijkstra
        es_dijkstra = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_dijkstra)

        if solo_aem and not es_aem:
            continue

        ancho = 2
        color = "#757575"
        patron_punteado = None

        if es_aem:
            color = "#2e7d32"  # Verde sólida (Kruskal)
            ancho = 4
        elif es_alt:
            color = "#0288d1"  # Azul punteada
            ancho = 3
            patron_punteado = (4, 4)
        elif es_cic:
            color = "#c62828"  # Rojo punteado
            ancho = 2
            patron_punteado = (4, 4)

        # Estilo para los arcos del camino mínimo de Dijkstra
        if es_dijkstra:
            color = "#6a1b9a"  # Morado/Púrpura distintivo para Dijkstra
            ancho = 4
            patron_punteado = None

        if arco_evaluando and ((u == arco_evaluando[0] and v == arco_evaluando[1]) or
                               (v == arco_evaluando[0] and u == arco_evaluando[1])):
            if estado_evaluacion == "EVALUANDO":
                color = "#fbc02d"
                ancho = 4
                patron_punteado = None
            elif estado_evaluacion == "RECHAZADO":
                color = "#c62828"
                ancho = 3
                patron_punteado = (4, 4)

        x1, y1 = grafo.nodos[u]
        x2, y2 = grafo.nodos[v]

        if patron_punteado:
            canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho, dash=patron_punteado)
        else:
            canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)

        # Etiqueta Peso
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_rectangle(mx - 14, my - 10, mx + 14, my + 10, fill="#ffffff", outline="#bdbdbd")
        texto_peso = f"{int(w)}" if w.is_integer() else f"{w:.1f}"
        canvas.create_text(mx, my, text=texto_peso, fill="#000000", font=("Arial", 9, "bold"))

    # 2. Dibujar Nodos
    radio = 18
    for nombre, (x, y) in grafo.nodos.items():
        if solo_aem and resultado_aem:
            nodos_en_aem = set()
            for u, v, _ in arcos_aem:
                nodos_en_aem.add(u)
                nodos_en_aem.add(v)
            if nombre not in nodos_en_aem and len(grafo.nodos) > 1:
                continue

        color_fondo = "#81d4fa"
        color_borde = "#0277bd"
        ancho_borde = 2

        # Resaltado según selección o si es Nodo Origen de Dijkstra
        if nombre == nodo_seleccionado:
            color_fondo = "#ffb74d"  # Naranja de selección

        if origen_dijkstra and nombre == origen_dijkstra:
            color_fondo = "#ffe082"  # Amarillo/Dorado para el Origen
            color_borde = "#e65100"  # Borde naranja oscuro
            ancho_borde = 3

        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_fondo, outline=color_borde,
                           width=ancho_borde)

        # Si se ejecutó Dijkstra, mostrar el nombre y la distancia d[v] debajo del nodo
        if distancias_dijkstra and nombre in distancias_dijkstra:
            dist = distancias_dijkstra[nombre]
            dist_str = f"{int(dist)}" if isinstance(dist, (int, float)) and dist != float(
                'inf') and dist.is_integer() else (str(dist) if dist != float('inf') else "∞")
            texto_nodo = f"{nombre}\n[d={dist_str}]"
            canvas.create_text(x, y, text=texto_nodo, fill="#000000", font=("Arial", 8, "bold"))
        else:
            canvas.create_text(x, y, text=nombre, fill="#000000", font=("Arial", 10, "bold"))

    # 3. Mostrar Información General
    # AEM (Kruskal)
    if resultado_aem is not None:
        texto_aem = f"PESO TOTAL AEM: {peso_total:.2f}" if not peso_total.is_integer() else f"PESO TOTAL AEM: {int(peso_total)}"
        canvas.create_rectangle(10, 10, 260, 45, fill="#e8f5e9", outline="#2e7d32", width=2)
        canvas.create_text(135, 27, text=texto_aem, fill="#1b5e20", font=("Arial", 12, "bold"))

    # Dijkstra
    if resultado_dijkstra is not None:
        texto_dijkstra = f"DIJKSTRA (Origen: {origen_dijkstra})"
        canvas.create_rectangle(10, 10, 260, 45, fill="#f3e5f5", outline="#6a1b9a", width=2)
        canvas.create_text(135, 27, text=texto_dijkstra, fill="#4a148c", font=("Arial", 11, "bold"))