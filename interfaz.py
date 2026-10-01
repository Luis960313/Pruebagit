import tkinter as tk
from tkinter import messagebox, simpledialog

from dijkstra import ejecutar_dijkstra
from exportacion import exportar_imagen_canvas, exportar_informe_txt
from grafo import Grafo
from kruskal import UnionFind, ejecutar_kruskal
from visualizacion import redibujar_grafo


class InterfazAEM:

    def __init__(self, root):
        self.root = root
        self.root.title(
            "Árbol de Expansión Mínima (AEM) & Dijkstra - Investigación de Operaciones"
        )
        self.root.geometry("1100x750")

        self.grafo = Grafo()
        self.modo = "NODO"
        self.nodo_origen_arco = None
        self.nodo_arrastrado = None

        # Almacenamiento de resultados
        self.resultado_aem = None
        self.resultado_dijkstra = None
        self.nodo_origen_dijkstra = None

        self.animando = False

        self._crear_interfaz()

    def _crear_interfaz(self):
        panel_superior = tk.Frame(
            self.root, bg="#f0f0f0", bd=2, relief=tk.RAISED
        )
        panel_superior.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Botones de modo
        tk.Button(
            panel_superior,
            text="➕ Agregar Nodo",
            command=lambda: self._cambiar_modo("NODO"),
            bg="#e1f5fe",
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="🔗 Crear Arco",
            command=lambda: self._cambiar_modo("ARCO"),
            bg="#e1f5fe",
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="✋ Mover Nodo",
            command=lambda: self._cambiar_modo("MOVER"),
            bg="#e1f5fe",
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="🗑️ Eliminar Elemento",
            command=lambda: self._cambiar_modo("ELIMINAR"),
            bg="#ffebee",
        ).pack(side=tk.LEFT, padx=3)

        tk.Label(panel_superior, text="|", bg="#f0f0f0").pack(
            side=tk.LEFT, padx=3
        )

        tk.Button(
            panel_superior,
            text="🎲 Red Aleatoria",
            command=self._generar_aleatorio,
            bg="#fff9c4",
        ).pack(side=tk.LEFT, padx=3)

        # Botones Kruskal (AEM)
        tk.Button(
            panel_superior,
            text="⚡ Calcular AEM",
            command=self._ejecutar_directo,
            bg="#c8e6c9",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="▶️ AEM Paso a Paso",
            command=self._ejecutar_paso_a_paso,
            bg="#a5d6a7",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.LEFT, padx=3)

        tk.Label(panel_superior, text="|", bg="#f0f0f0").pack(
            side=tk.LEFT, padx=3
        )

        # Botón para Dijkstra (Requisito del Documento)
        tk.Button(
            panel_superior,
            text="🚩 Ejecutar Dijkstra",
            command=self._ejecutar_dijkstra_interfaz,
            bg="#e1bee7",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.LEFT, padx=3)

        tk.Label(panel_superior, text="|", bg="#f0f0f0").pack(
            side=tk.LEFT, padx=3
        )

        # Opciones de Guardado
        tk.Button(
            panel_superior,
            text="🖼️️ Exportar Grafo",
            command=lambda: exportar_imagen_canvas(
                self.canvas, self.grafo, self.resultado_aem, solo_aem=False
            ),
            bg="#e0f7fa",
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="🌳 Guardar Red AEM",
            command=lambda: exportar_imagen_canvas(
                self.canvas, self.grafo, self.resultado_aem, solo_aem=True
            ),
            bg="#b2dfdb",
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            panel_superior,
            text="📄 Exportar (.TXT)",
            command=lambda: exportar_informe_txt(
                self.grafo, self.resultado_aem
            ),
            bg="#e8eaf6",
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            panel_superior,
            text="🔄 Reiniciar",
            command=self._reiniciar,
            bg="#ffcdd2",
        ).pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas.bind("<ButtonPress-1>", self._al_clic)
        self.canvas.bind("<B1-Motion>", self._al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self._al_soltar)

        self.lbl_estado = tk.Label(
            self.root,
            text="Modo: Agregar Nodo | Haz clic para colocar nodos.",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 10),
            bg="#ffffff",
        )
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _cambiar_modo(self, modo):
        if self.animando:
            return
        self.modo = modo
        self.nodo_origen_arco = None
        self._actualizar()

    def _limpiar_resultados(self):
        """Limpia los resultados calculados al modificar el grafo."""
        self.resultado_aem = None
        self.resultado_dijkstra = None
        self.nodo_origen_dijkstra = None

    def _al_clic(self, event):
        if self.animando:
            return

        ancho_canvas = max(100, self.canvas.winfo_width())
        alto_canvas = max(100, self.canvas.winfo_height())
        margen = 25

        x = max(margen, min(event.x, ancho_canvas - margen))
        y = max(margen, min(event.y, alto_canvas - margen))

        nodo = self.grafo.obtener_nodo_en_posicion(x, y)
        arco_clicado = self.grafo.obtener_arco_en_posicion(x, y)

        if self.modo == "NODO" and not nodo:
            self.grafo.agregar_nodo(
                x, y, margen=margen, ancho_max=ancho_canvas, alto_max=alto_canvas
            )
            self._limpiar_resultados()
            self._actualizar()

        elif self.modo == "ARCO":
            if arco_clicado and not nodo:
                u, v, peso_actual = arco_clicado
                nuevo_peso = simpledialog.askfloat(
                    "Modificar Peso",
                    f"Modificar el peso del arco ({u} - {v}):",
                    initialvalue=peso_actual,
                    minvalue=0.0,  # Previene pesos negativos (Validación Dijkstra)
                )
                if nuevo_peso is not None:
                    self.grafo.eliminar_arco(arco_clicado)
                    self.grafo.agregar_arco(u, v, nuevo_peso)
                    self._limpiar_resultados()
                    self._actualizar()
                return

            if nodo:
                if not self.nodo_origen_arco:
                    self.nodo_origen_arco = nodo
                else:
                    u, v = self.nodo_origen_arco, nodo
                    self.nodo_origen_arco = None

                    if u != v:
                        if self.grafo.existe_arco(u, v):
                            if messagebox.askyesno(
                                "Arco Existente",
                                f"El arco entre {u} y {v} ya existe.\n¿Deseas modificar su peso?",
                            ):
                                peso_actual = next(
                                    w
                                    for n1, n2, w in self.grafo.arcos
                                    if (n1 == u and n2 == v)
                                    or (n1 == v and n2 == u)
                                )
                                nuevo_peso = simpledialog.askfloat(
                                    "Modificar Peso",
                                    f"Ingrese el nuevo peso para ({u} - {v}):",
                                    initialvalue=peso_actual,
                                    minvalue=0.0,
                                )
                                if nuevo_peso is not None:
                                    self.grafo.eliminar_arco((u, v, peso_actual))
                                    self.grafo.eliminar_arco((v, u, peso_actual))
                                    self.grafo.agregar_arco(u, v, nuevo_peso)
                                    self._limpiar_resultados()
                        else:
                            peso = simpledialog.askfloat(
                                "Peso",
                                f"Ingrese el peso ({u} - {v}):",
                                minvalue=0.0,
                            )
                            if peso is not None:
                                self.grafo.agregar_arco(u, v, peso)
                                self._limpiar_resultados()
            self._actualizar()

        elif self.modo == "MOVER" and nodo:
            self.nodo_arrastrado = nodo

        elif self.modo == "ELIMINAR":
            if nodo:
                self.grafo.eliminar_nodo(nodo)
            elif arco_clicado:
                self.grafo.eliminar_arco(arco_clicado)
            self._limpiar_resultados()
            self._actualizar()

    def _al_arrastrar(self, event):
        if self.modo == "MOVER" and self.nodo_arrastrado:
            ancho_canvas = max(100, self.canvas.winfo_width())
            alto_canvas = max(100, self.canvas.winfo_height())
            margen = 25

            x_limitado = max(margen, min(event.x, ancho_canvas - margen))
            y_limitado = max(margen, min(event.y, alto_canvas - margen))

            self.grafo.nodos[self.nodo_arrastrado] = (x_limitado, y_limitado)
            self._actualizar()

    def _al_soltar(self, event):
        self.nodo_arrastrado = None

    def _actualizar(self):
        redibujar_grafo(
            self.canvas,
            self.grafo,
            resultado_aem=self.resultado_aem,
            nodo_seleccionado=self.nodo_origen_arco,
            resultado_dijkstra=self.resultado_dijkstra,
            nodo_origen_dijkstra=self.nodo_origen_dijkstra,
        )

    def _generar_aleatorio(self):
        cant = simpledialog.askinteger(
            "Red Aleatoria", "Cantidad de nodos (4-12):", minvalue=4, maxvalue=12
        )
        if cant:
            self.grafo.generar_red_aleatoria(
                cant, self.canvas.winfo_width(), self.canvas.winfo_height()
            )
            self._limpiar_resultados()
            self._actualizar()

    def _ejecutar_directo(self):
        conexa, msg = self.grafo.es_red_conexa()
        if not conexa:
            messagebox.showerror("Error", msg)
            return
        self.resultado_dijkstra = None
        self.resultado_aem = ejecutar_kruskal(
            list(self.grafo.nodos.keys()), self.grafo.arcos
        )
        self._actualizar()

    def _ejecutar_paso_a_paso(self):
        conexa, msg = self.grafo.es_red_conexa()
        if not conexa:
            messagebox.showerror("Error", msg)
            return

        self.resultado_dijkstra = None
        self.animando = True
        arcos_ordenados = sorted(self.grafo.arcos, key=lambda x: x[2])
        uf = UnionFind(list(self.grafo.nodos.keys()))

        aem_temp, cic_temp = [], []

        def generador():
            for u, v, w in arcos_ordenados:
                redibujar_grafo(
                    self.canvas,
                    self.grafo,
                    {
                        "aem": aem_temp,
                        "alternativos": [],
                        "ciclos": cic_temp,
                        "peso_total": sum(x[2] for x in aem_temp),
                    },
                    arco_evaluando=(u, v, w),
                    estado_evaluacion="EVALUANDO",
                )
                yield
                if uf.find(u) != uf.find(v):
                    uf.union(u, v)
                    aem_temp.append((u, v, w))
                else:
                    cic_temp.append((u, v, w))
                redibujar_grafo(
                    self.canvas,
                    self.grafo,
                    {
                        "aem": aem_temp,
                        "alternativos": [],
                        "ciclos": cic_temp,
                        "peso_total": sum(x[2] for x in aem_temp),
                    },
                )
                yield

            self.resultado_aem = ejecutar_kruskal(
                list(self.grafo.nodos.keys()), self.grafo.arcos
            )
            self.animando = False
            self._actualizar()

        gen = generador()

        def paso():
            try:
                next(gen)
                self.root.after(1000, paso)
            except StopIteration:
                pass

        paso()

    def _ejecutar_dijkstra_interfaz(self):
        """Ejecuta el algoritmo de Dijkstra solicitando el nodo de origen."""
        if not self.grafo.nodos:
            messagebox.showwarning(
                "Grafo Vacío",
                "Debe agregar nodos a la red para ejecutar Dijkstra.",
            )
            return

        nodos_disponibles = list(self.grafo.nodos.keys())
        origen = simpledialog.askstring(
            "Nodo Origen - Dijkstra",
            f"Ingrese el nodo de origen para el algoritmo:\nNodos disponibles: {', '.join(nodos_disponibles)}",
        )

        if not origen:
            return

        origen = origen.strip()
        if origen not in self.grafo.nodos:
            messagebox.showerror(
                "Nodo Inválido",
                f"El nodo '{origen}' no existe en la red actual.",
            )
            return

        try:
            self.resultado_aem = None  # Limpiar AEM al ejecutar Dijkstra
            self.resultado_dijkstra = ejecutar_dijkstra(self.grafo, origen)
            self.nodo_origen_dijkstra = origen
            self._actualizar()

            # Mostrar informe modal con los caminos y distancias mínimas obtenidas
            self._mostrar_resumen_dijkstra(origen)

        except ValueError as err:
            messagebox.showerror("Error de Validación", str(err))

    def _mostrar_resumen_dijkstra(self, origen):
        """Muestra un diálogo flotante con las distancias mínimas y los recorridos."""
        distancias = self.resultado_dijkstra["distancias"]
        caminos = self.resultado_dijkstra["caminos"]

        lineas = [f"=== RESULTADOS DIJKSTRA (Origen: {origen}) ===\n"]

        for nodo, dist in distancias.items():
            if dist == float("inf"):
                lineas.append(f"• Nodo {nodo}: INALCANZABLE desde el origen")
            else:
                camino_str = " ➔ ".join(caminos[nodo])
                dist_str = f"{int(dist)}" if isinstance(dist, float) and dist.is_integer() else f"{dist}"
                lineas.append(
                    f"• Nodo {nodo}: Distancia Mínima = {dist_str} | Ruta: [{camino_str}]"
                )

        messagebox.showinfo("Resultados de Dijkstra", "\n".join(lineas))

    def _reiniciar(self):
        if messagebox.askyesno("Confirmar", "¿Deseas reiniciar la red?"):
            self.grafo = Grafo()
            self._limpiar_resultados()
            self._actualizar()