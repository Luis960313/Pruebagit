import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from dijkstra import ejecutar_dijkstra
from exportacion import exportar_imagen_canvas, exportar_informe_txt
from grafo import Grafo
from kruskal import UnionFind, ejecutar_kruskal
from visualizacion import redibujar_grafo


class InterfazAEM:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Redes: AEM (Kruskal) & Dijkstra")
        self.root.geometry("1150x780")

        self.grafo = Grafo()
        self.modo = "NODO"  # Modos: NODO, ARCO, MOVER, ORIGEN_DIJKSTRA, ELIMINAR
        self.nodo_origen_arco = None
        self.nodo_arrastrado = None

        self.resultado_aem = None
        self.resultado_dijkstra = None
        self.nodo_origen_dijkstra = None

        self.animando = False

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel Superior
        panel_superior = tk.Frame(self.root, bg="#f5f5f5", bd=2, relief=tk.RAISED)
        panel_superior.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Botones de Edición Básica
        tk.Button(panel_superior, text="➕ Agregar Nodo", command=lambda: self._cambiar_modo("NODO"), bg="#e1f5fe").pack(
            side=tk.LEFT, padx=2)
        tk.Button(panel_superior, text="🔗 Crear Arco", command=lambda: self._cambiar_modo("ARCO"), bg="#e1f5fe").pack(
            side=tk.LEFT, padx=2)
        tk.Button(panel_superior, text="✋ Mover Nodo", command=lambda: self._cambiar_modo("MOVER"), bg="#e1f5fe").pack(
            side=tk.LEFT, padx=2)
        tk.Button(panel_superior, text="🗑️ Eliminar", command=lambda: self._cambiar_modo("ELIMINAR"),
                  bg="#ffebee").pack(side=tk.LEFT, padx=2)

        tk.Label(panel_superior, text="|", bg="#f5f5f5").pack(side=tk.LEFT, padx=2)

        # Generador Aleatorio
        tk.Button(panel_superior, text="🎲 Red Aleatoria", command=self._generar_aleatorio, bg="#fff9c4").pack(
            side=tk.LEFT, padx=2)

        tk.Label(panel_superior, text="|", bg="#f5f5f5").pack(side=tk.LEFT, padx=2)

        # Botones Kruskal (AEM)
        tk.Button(panel_superior, text="⚡ AEM Directo", command=self._ejecutar_kruskal_directo, bg="#c8e6c9",
                  font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=2)
        tk.Button(panel_superior, text="▶️ AEM Paso a Paso", command=self._ejecutar_kruskal_paso_a_paso,
                  bg="#a5d6a7", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=2)

        tk.Label(panel_superior, text="|", bg="#f5f5f5").pack(side=tk.LEFT, padx=2)

        # Botón Dijkstra con Selección Gráfica (Mouse)
        tk.Button(panel_superior, text="🚩 Dijkstra",
                  command=lambda: self._cambiar_modo("ORIGEN_DIJKSTRA"), bg="#e1bee7", font=("Arial", 9, "bold")).pack(
            side=tk.LEFT, padx=2)

        tk.Label(panel_superior, text="|", bg="#f5f5f5").pack(side=tk.LEFT, padx=2)

        # Botón Reiniciar (SIEMPRE VISIBLE)
        tk.Button(panel_superior, text="🔄 Reiniciar", command=self._reiniciar, bg="#ffcdd2",
                  font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)

        # Opciones de Exportar/Guardar
        tk.Button(panel_superior, text="🖼️ Exportar Imagen",
                  command=lambda: exportar_imagen_canvas(self.canvas, self.grafo,
                                                         self.resultado_aem or self.resultado_dijkstra, solo_aem=False),
                  bg="#e0f7fa").pack(side=tk.LEFT, padx=2)
        tk.Button(panel_superior, text="📄 Exportar .TXT",
                  command=lambda: exportar_informe_txt(self.grafo, self.resultado_aem, self.resultado_dijkstra), bg="#e8eaf6").pack(side=tk.LEFT,
                                                                                                           padx=2)

        # Canvas Principal
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas.bind("<ButtonPress-1>", self._al_clic)
        self.canvas.bind("<B1-Motion>", self._al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self._al_soltar)

        # Barra de Estado Inferior
        self.lbl_estado = tk.Label(self.root, text="Modo: Agregar Nodo | Haz clic en la pantalla para crear nodos.",
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10), bg="#ffffff")
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _cambiar_modo(self, modo):
        if self.animando:
            return
        self.modo = modo
        self.nodo_origen_arco = None

        textos_modo = {
            "NODO": "Modo: Agregar Nodo | Haz clic para colocar un nuevo nodo.",
            "ARCO": (
                "Modo: Crear/Editar Arco | Clic en un arco para cambiar peso, o"
                " clic en dos nodos para unirlos."
            ),
            "MOVER": (
                "Modo: Mover Nodo | Arrastra un nodo para cambiar su posición."
            ),
            "ELIMINAR": (
                "Modo: Eliminar | Haz clic sobre un nodo o arco para borrarlo."
            ),
            "ORIGEN_DIJKSTRA": (
                "Modo: Dijkstra | Haz clic con el mouse sobre el NODO ORIGEN"
                " para calcular rutas."
            ),
        }

        # Actualiza el texto de la barra inferior
        self.lbl_estado.config(text=textos_modo.get(modo, ""))

        # Si el usuario selecciona el modo Dijkstra, muestra la ventana emergente con la instrucción
        if modo == "ORIGEN_DIJKSTRA":
            if not self.grafo.nodos:
                messagebox.showwarning(
                    "Grafo Vacío",
                    "Debe agregar nodos a la red antes de seleccionar un nodo"
                    " origen.",
                )
                self.modo = "NODO"
                self.lbl_estado.config(text=textos_modo["NODO"])
            else:
                messagebox.showinfo(
                    "Algoritmo de Dijkstra",
                    "Por favor, seleccione el NODO ORIGEN.",
                )

        self._actualizar()

    def _limpiar_resultados(self):
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

        # 1. Modo Agregar Nodo
        if self.modo == "NODO" and not nodo:
            self.grafo.agregar_nodo(x, y, margen=margen, ancho_max=ancho_canvas, alto_max=alto_canvas)
            self._limpiar_resultados()
            self._actualizar()

        # 2. Modo Crear / Modificar Arco
        elif self.modo == "ARCO":
            if arco_clicado and not nodo:
                u, v, peso_actual = arco_clicado
                nuevo_peso = simpledialog.askfloat(
                    "Modificar Peso",
                    f"Ingrese nuevo peso para ({u} - {v}):",
                    initialvalue=peso_actual,
                    minvalue=0.0  # Máximo 2 decimales, no negativo
                )
                if nuevo_peso is not None:
                    nuevo_peso = round(nuevo_peso, 2)
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
                            peso_actual = next(
                                w for n1, n2, w in self.grafo.arcos if (n1 == u and n2 == v) or (n1 == v and n2 == u))
                            nuevo_peso = simpledialog.askfloat("Modificar Peso", f"Modificar peso de ({u} - {v}):",
                                                               initialvalue=peso_actual, minvalue=0.0)
                            if nuevo_peso is not None:
                                self.grafo.eliminar_arco((u, v, peso_actual))
                                self.grafo.eliminar_arco((v, u, peso_actual))
                                self.grafo.agregar_arco(u, v, round(nuevo_peso, 2))
                                self._limpiar_resultados()
                        else:
                            peso = simpledialog.askfloat("Peso del Arco", f"Ingrese peso para ({u} - {v}):",
                                                         minvalue=0.0)
                            if peso is not None:
                                self.grafo.agregar_arco(u, v, round(peso, 2))
                                self._limpiar_resultados()
            self._actualizar()

        # 3. Modo Seleccionar Origen para Dijkstra directamente con el Mouse
        elif self.modo == "ORIGEN_DIJKSTRA":
            if nodo:
                self._ejecutar_dijkstra_desde_nodo(nodo)
            else:
                messagebox.showinfo("Selección",
                                    "Haz clic sobre uno de los nodos circulares para elegirlo como Origen.")

        # 4. Modo Mover
        elif self.modo == "MOVER" and nodo:
            self.nodo_arrastrado = nodo

        # 5. Modo Eliminar
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
            nodo_origen_dijkstra=self.nodo_origen_dijkstra
        )

    def _generar_aleatorio(self):
        cant = simpledialog.askinteger("Red Aleatoria", "Cantidad de nodos (4-12):", minvalue=4, maxvalue=12)
        if cant:
            self.grafo.generar_red_aleatoria(cant, self.canvas.winfo_width(), self.canvas.winfo_height())
            self._limpiar_resultados()
            self._actualizar()

    def _ejecutar_kruskal_directo(self):
        conexa, msg = self.grafo.es_red_conexa()
        if not conexa:
            messagebox.showerror("Error", msg)
            return
        self.resultado_dijkstra = None
        self.nodo_origen_dijkstra = None
        self.resultado_aem = ejecutar_kruskal(list(self.grafo.nodos.keys()), self.grafo.arcos)
        self._actualizar()

    def _ejecutar_kruskal_paso_a_paso(self):
        conexa, msg = self.grafo.es_red_conexa()
        if not conexa:
            messagebox.showerror("Error", msg)
            return

        self.resultado_dijkstra = None
        self.nodo_origen_dijkstra = None
        self.animando = True
        arcos_ordenados = sorted(self.grafo.arcos, key=lambda x: x[2])
        uf = UnionFind(list(self.grafo.nodos.keys()))

        aem_temp, cic_temp = [], []

        def generador():
            for u, v, w in arcos_ordenados:
                redibujar_grafo(self.canvas, self.grafo, {"aem": aem_temp, "alternativos": [], "ciclos": cic_temp,
                                                          "peso_total": sum(x[2] for x in aem_temp)},
                                arco_evaluando=(u, v, w), estado_evaluacion="EVALUANDO")
                yield
                if uf.find(u) != uf.find(v):
                    uf.union(u, v)
                    aem_temp.append((u, v, w))
                else:
                    cic_temp.append((u, v, w))
                redibujar_grafo(self.canvas, self.grafo, {"aem": aem_temp, "alternativos": [], "ciclos": cic_temp,
                                                          "peso_total": sum(x[2] for x in aem_temp)})
                yield

            self.resultado_aem = ejecutar_kruskal(list(self.grafo.nodos.keys()), self.grafo.arcos)
            self.animando = False
            self._actualizar()

        gen = generador()

        def paso():
            try:
                next(gen)
                self.root.after(800, paso)
            except StopIteration:
                pass

        paso()

    def _ejecutar_dijkstra_desde_nodo(self, origen):
        """Ejecuta Dijkstra tomando el nodo origen seleccionado directamente."""
        try:
            self.resultado_aem = None  # Limpiar AEM
            self.resultado_dijkstra = ejecutar_dijkstra(self.grafo, origen)
            self.nodo_origen_dijkstra = origen
            self._actualizar()

            # Mostrar reporte estructurado elegante
            self._mostrar_reporte_dijkstra_elegante(origen)

        except ValueError as err:
            messagebox.showerror("Error en Dijkstra", str(err))

    def _mostrar_reporte_dijkstra_elegante(self, origen):
        """Abre una ventana emergente organizada y formal con la tabla de resultados."""
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Resultados Algoritmo de Dijkstra - Origen: [{origen}]")
        ventana.geometry("550x380")
        ventana.resizable(False, False)

        tk.Label(ventana, text=f"CAMINOS MÍNIMOS DESDE NODO ORIGEN: {origen}", font=("Arial", 11, "bold"), bg="#6a1b9a",
                 fg="white", pady=8).pack(fill=tk.X)

        frame_tabla = tk.Frame(ventana, padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        # Tabla (Treeview)
        columnas = ("nodo", "distancia", "recorrido")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        tabla.heading("nodo", text="Nodo Destino")
        tabla.heading("distancia", text="Distancia Mínima")
        tabla.heading("recorrido", text="Secuencia / Recorrido")

        tabla.column("nodo", width=100, anchor="center")
        tabla.column("distancia", width=120, anchor="center")
        tabla.column("recorrido", width=280, anchor="w")

        distancias = self.resultado_dijkstra["distancias"]
        caminos = self.resultado_dijkstra["caminos"]

        for nodo, dist in distancias.items():
            if dist == float("inf"):
                tabla.insert("", tk.END, values=(nodo, "INALCANZABLE", "Sin Ruta"))
            else:
                dist_str = f"{int(dist)}" if isinstance(dist, (int, float)) and dist.is_integer() else f"{dist:.2f}"
                ruta_str = " ➔ ".join(caminos[nodo])
                tabla.insert("", tk.END, values=(nodo, dist_str, ruta_str))

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tabla.pack(fill=tk.BOTH, expand=True)

        tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#e0e0e0", font=("Arial", 9, "bold"),
                  width=12).pack(pady=8)

    def _reiniciar(self):
        if messagebox.askyesno("Confirmar Reinicio", "¿Deseas borrar toda la red y comenzar desde cero?"):
            self.grafo = Grafo()
            self._limpiar_resultados()
            self.modo = "NODO"
            self.lbl_estado.config(text="Modo: Agregar Nodo | Haz clic para colocar nodos.")
            self._actualizar()