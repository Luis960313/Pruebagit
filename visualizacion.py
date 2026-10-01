"""
Módulo para el renderizado gráfico del grafo y sus algoritmos en Tkinter Canvas.
"""


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

        # Identificar si pertenece al camino mínimo de Dijkstra
        es_dijkstra = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_dijkstra)

        if solo_aem and not es_aem and not es_dijkstra:
            continue

        ancho = 2
        color = "#757575"
        patron_punteado = None

        if es_aem:
            color = "#2e7d32"  # Verde (Kruskal)
            ancho = 4
        elif es_alt:
            color = "#0288d1"  # Azul
            ancho = 3
            patron_punteado = (4, 4)
        elif es_cic:
            color = "#c62828"  # Rojo
            ancho = 2
            patron_punteado = (4, 4)

        # Estilo para el camino mínimo de Dijkstra
        if es_dijkstra:
            color = "#6a1b9a"  # Morado
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

        # Etiqueta del Peso (Formateado con máximo 2 decimales)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        texto_peso = f"{int(w)}" if w.is_integer() else f"{w:.2f}"

        canvas.create_rectangle(mx - 16, my - 10, mx + 16, my + 10, fill="#ffffff", outline="#bdbdbd")
        canvas.create_text(mx, my, text=texto_peso, fill="#000000", font=("Arial", 9, "bold"))

    # 2. Dibujar Nodos
    radio = 22  # Radio ampliado para mejor visibilidad
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

        # Nodo Seleccionado
        if nombre == nodo_seleccionado:
            color_fondo = "#ffb74d"

        # Nodo Origen de Dijkstra
        if origen_dijkstra and nombre == origen_dijkstra:
            color_fondo = "#ffd54f"  # Amarillo/Dorado
            color_borde = "#e65100"  # Naranja oscuro
            ancho_borde = 3

        # Circulo del Nodo
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_fondo, outline=color_borde,
                           width=ancho_borde)
        # Nombre del Nodo en el centro
        canvas.create_text(x, y, text=str(nombre), fill="#000000", font=("Arial", 11, "bold"))

        # Etiqueta Flotante de Distancia Mínima d[v] (Dijkstra)
        if distancias_dijkstra and nombre in distancias_dijkstra:
            dist = distancias_dijkstra[nombre]
            if dist == float('inf'):
                dist_str = "d = ∞"
                color_tag = "#ffebee"
                color_texto = "#c62828"
            else:
                dist_str = f"d = {int(dist)}" if isinstance(dist,
                                                            (int, float)) and dist.is_integer() else f"d = {dist:.2f}"
                color_tag = "#e8f5e9" if dist == 0 else "#f3e5f5"
                color_texto = "#1b5e20" if dist == 0 else "#4a148c"

            # Dibujar un recuadro indicativo arriba del nodo
            canvas.create_rectangle(x - 24, y - radio - 20, x + 24, y - radio - 3, fill=color_tag, outline="#ab47bc",
                                    width=1)
            canvas.create_text(x, y - radio - 11, text=dist_str, fill=color_texto, font=("Arial", 9, "bold"))

    # 3. Cartel Informativo
    if resultado_aem is not None:
        texto_aem = f"PESO TOTAL AEM: {peso_total:.2f}" if not peso_total.is_integer() else f"PESO TOTAL AEM: {int(peso_total)}"
        canvas.create_rectangle(10, 10, 260, 45, fill="#e8f5e9", outline="#2e7d32", width=2)
        canvas.create_text(135, 27, text=texto_aem, fill="#1b5e20", font=("Arial", 11, "bold"))

    if resultado_dijkstra is not None:
        texto_dijkstra = f"DIJKSTRA (Origen: {origen_dijkstra})"
        canvas.create_rectangle(10, 10, 260, 45, fill="#f3e5f5", outline="#6a1b9a", width=2)
        canvas.create_text(135, 27, text=texto_dijkstra, fill="#4a148c", font=("Arial", 11, "bold"))