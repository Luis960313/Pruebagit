def redibujar_grafo(canvas, grafo, resultado_aem=None, nodo_seleccionado=None,
                    arco_evaluando=None, estado_evaluacion=None, solo_aem=False):
    canvas.delete("all")

    arcos_aem = resultado_aem["aem"] if resultado_aem else []
    arcos_alt = resultado_aem["alternativos"] if resultado_aem else []
    arcos_cic = resultado_aem["ciclos"] if resultado_aem else []
    peso_total = resultado_aem["peso_total"] if resultado_aem else 0.0

    # 1. Dibujar Arcos
    for u, v, w in grafo.arcos:
        es_aem = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_aem)
        es_alt = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_alt)
        es_cic = any((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u) for a in arcos_cic)

        if solo_aem and not es_aem:
            continue

        ancho = 2
        color = "#757575"
        patron_punteado = None

        if es_aem:
            color = "#2e7d32"  # Verde sólida
            ancho = 4
        elif es_alt:
            color = "#0288d1"  # Azul punteada (Alternativa por empate)
            ancho = 3
            patron_punteado = (4, 4)
        elif es_cic:
            color = "#c62828"  # Rojo punteado
            ancho = 2
            patron_punteado = (4, 4)

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
        if nombre == nodo_seleccionado:
            color_fondo = "#ffb74d"

        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_fondo, outline="#0277bd", width=2)
        canvas.create_text(x, y, text=nombre, fill="#000000", font=("Arial", 10, "bold"))

    # 3. Mostrar Peso Total
    if resultado_aem is not None:
            texto_aem = f"PESO TOTAL AEM: {peso_total:.2f}" if not peso_total.is_integer() else f"PESO TOTAL AEM: {int(peso_total)}"
            canvas.create_rectangle(10, 10, 260, 45, fill="#e8f5e9", outline="#2e7d32", width=2)
            canvas.create_text(135, 27, text=texto_aem, fill="#1b5e20", font=("Arial", 12, "bold"))