from tkinter import filedialog, messagebox
from visualizacion import redibujar_grafo


def exportar_informe_txt(grafo, resultado_aem):
    if not grafo.nodos:
        messagebox.showwarning("Atención", "No hay datos en la red para exportar.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de Texto", "*.txt")],
        title="Guardar Informe del AEM"
    )
    if not filepath:
        return

    aem = resultado_aem["aem"] if resultado_aem else []
    alt = resultado_aem["alternativos"] if resultado_aem else []
    cic = resultado_aem["ciclos"] if resultado_aem else []
    historial = resultado_aem["historial"] if resultado_aem else []
    peso_total = resultado_aem["peso_total"] if resultado_aem else 0.0

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 65 + "\n")
            f.write("        ARBOL DE EXPANSION MINIMA (AEM)\n")
            f.write("=" * 65 + "\n\n")

            f.write(f"Cantidad de nodos: {len(grafo.nodos)}\n")
            f.write(f"Cantidad de aristas: {len(grafo.arcos)}\n\n")

            f.write("Aristas seleccionadas:\n")
            for u, v, w in aem:
                f.write(f"  ✓ {u} - {v} : {w}\n")

            f.write(f"\nCosto total: {peso_total}\n\n")

            if alt:
                f.write("Aristas alternativas por empate:\n")
                for u, v, w in alt:
                    f.write(f"  ┄ {u} - {v} : {w}\n")
                f.write("\n")

            f.write("Aristas descartadas por ciclo:\n")
            for u, v, w in cic:
                f.write(f"  ✗ {u} - {v} : {w}\n")

            f.write("\n" + "=" * 65 + "\n")
            f.write("REGISTRO PASO A PASO\n")
            f.write("=" * 65 + "\n")
            for paso in historial:
                f.write(f"  {paso}\n")

        messagebox.showinfo("Éxito", f"Informe guardado en:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")


def exportar_imagen_canvas(canvas, grafo, resultado_aem, solo_aem=False):
    if not grafo.nodos:
        messagebox.showwarning("Atención", "No hay ningún grafo para exportar.")
        return

    titulo = "Guardar Imagen del AEM Final" if solo_aem else "Guardar Grafo Completo"
    filepath = filedialog.asksaveasfilename(
        defaultextension=".ps",
        filetypes=[("PostScript", "*.ps")],
        title=titulo
    )
    if filepath:
        try:
            if solo_aem:
                redibujar_grafo(canvas, grafo, resultado_aem, solo_aem=True)

            canvas.postscript(file=filepath, colormode="color")

            if solo_aem:
                redibujar_grafo(canvas, grafo, resultado_aem, solo_aem=False)

            messagebox.showinfo("Éxito", f"Imagen exportada en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {str(e)}")