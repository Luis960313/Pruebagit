"""
Módulo para la exportación del grafo y los resultados de los algoritmos (AEM y Dijkstra)
a archivos de imagen y reportes de texto.
"""
from tkinter import filedialog, messagebox


def exportar_imagen_canvas(canvas, grafo, resultado=None, solo_aem=False):
    """Guarda una captura/imagen PostScript (.ps) del Canvas actual

    validando previamente que el grafo contenga elementos.
    """
    # Validar que existan nodos en el grafo
    if not grafo.nodos:
        messagebox.showwarning(
            "Red Vacía",
            "No hay elementos en la red para exportar una imagen."
        )
        return

    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript Files", "*.ps"), ("All Files", "*.*")],
            title="Guardar Grafo como Imagen"
        )
        if filepath:
            canvas.postscript(file=filepath, colormode="color")
            messagebox.showinfo(
                "Exportación Exitosa",
                f"La imagen de la red fue guardada correctamente en:\n{filepath}"
            )
    except Exception as e:
        messagebox.showerror(
            "Error al Exportar",
            f"No se pudo guardar la imagen:\n{str(e)}"
        )


def exportar_informe_txt(grafo, resultado_aem=None, resultado_dijkstra=None):
    """Genera y guarda un reporte en formato .txt con el estado de la red

    y los resultados de Kruskal (AEM) y/o Dijkstra según corresponda.
    Validando previamente que la red tenga elementos.
    """
    # Validar que existan nodos en el grafo
    if not grafo.nodos:
        messagebox.showwarning(
            "Red Vacía",
            "No hay elementos en la red para exportar un informe."
        )
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Exportar Informe de la Red (.TXT)"
    )

    if not filepath:
        return

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("====================================================\n")
            f.write("      REPORTE DE RED Y ALGORITMOS DE OPTIMIZACIÓN   \n")
            f.write("====================================================\n\n")

            # 1. Estructura de la Red
            f.write("1. ESTRUCTURA DE LA RED\n")
            f.write(f"   - Cantidad total de nodos: {len(grafo.nodos)}\n")
            f.write(f"   - Cantidad total de arcos: {len(grafo.arcos)}\n\n")

            f.write("   Listado de Nodos:\n")
            for nombre, (x, y) in grafo.nodos.items():
                f.write(f"     • Nodo {nombre} -> Posición: ({x}, {y})\n")
            f.write("\n")

            f.write("   Listado de Arcos y Pesos:\n")
            for u, v, w in grafo.arcos:
                w_str = f"{int(w)}" if w.is_integer() else f"{w:.2f}"
                f.write(f"     • Arco ({u} - {v}) | Peso: {w_str}\n")
            f.write("\n" + "-" * 52 + "\n\n")

            # 2. Resultados de Kruskal (AEM)
            if resultado_aem:
                f.write("2. RESULTADOS: ÁRBOL DE EXPANSIÓN MÍNIMA (KRUSKAL)\n")
                arcos_aem = resultado_aem.get("aem", [])
                peso_total = resultado_aem.get("peso_total", 0.0)

                peso_str = f"{int(peso_total)}" if peso_total.is_integer() else f"{peso_total:.2f}"
                f.write(f"   - Peso Total del Árbol de Expansión Mínima: {peso_str}\n")
                f.write("   - Arcos pertenecientes al AEM:\n")
                for u, v, w in arcos_aem:
                    w_str = f"{int(w)}" if w.is_integer() else f"{w:.2f}"
                    f.write(f"     • ({u} - {v}) con peso {w_str}\n")
                f.write("\n" + "-" * 52 + "\n\n")

            # 3. Resultados de Dijkstra
            if resultado_dijkstra:
                origen = resultado_dijkstra.get("origen", "Desconocido")
                distancias = resultado_dijkstra.get("distancias", {})
                caminos = resultado_dijkstra.get("caminos", {})

                f.write("3. RESULTADOS: CAMINOS MÍNIMOS (ALGORITMO DE DIJKSTRA)\n")
                f.write(f"   - Nodo Origen Seleccionado: [{origen}]\n\n")
                f.write("   Tabla de Distancias y Rutas Mínimas:\n")

                for nodo, dist in distancias.items():
                    if dist == float("inf"):
                        f.write(f"     • Hacia Nodo {nodo}: INALCANZABLE (Sin Ruta)\n")
                    else:
                        dist_str = f"{int(dist)}" if isinstance(dist, (int, float)) and dist.is_integer() else f"{dist:.2f}"
                        ruta_str = " -> ".join(caminos[nodo])
                        f.write(f"     • Hacia Nodo {nodo}: Distancia Mínima = {dist_str} | Ruta: [{ruta_str}]\n")
                f.write("\n" + "-" * 52 + "\n\n")

            if not resultado_aem and not resultado_dijkstra:
                f.write("2. RESULTADOS DE ALGORITMOS\n")
                f.write("   (No se ha ejecutado ningún algoritmo sobre esta red aún)\n\n")

        messagebox.showinfo(
            "Exportación Exitosa",
            f"El informe en texto fue guardado correctamente en:\n{filepath}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error al Exportar",
            f"No se pudo guardar el informe:\n{str(e)}"
        )