import math
import random


class Grafo:

    def __init__(self):
        self.nodos = {}  # {id_nodo: (x, y)}
        self.arcos = []  # [(u, v, peso), ...]
        self.contador_nodos = 0  # Índice base para convertir a letras

    def _generar_nombre_nodo(self):
        """Genera nombres secuenciales alfabéticos en mayúsculas:

        0 -> A, 1 -> B, ..., 25 -> Z, 26 -> AA, 27 -> AB, ...
        """
        temp = self.contador_nodos
        nombre = ""
        while temp >= 0:
            nombre = chr(65 + (temp % 26)) + nombre
            temp = (temp // 26) - 1
        return nombre

    def agregar_nodo(self, x, y, margen=25, ancho_max=1000, alto_max=700):
        # Restringir x e y dentro de los límites visibles
        x_limitado = max(margen, min(x, ancho_max - margen))
        y_limitado = max(margen, min(y, alto_max - margen))

        # Generar nombre alfabético
        nombre = self._generar_nombre_nodo()

        # Evitar duplicados si ya existe el nombre
        while nombre in self.nodos:
            self.contador_nodos += 1
            nombre = self._generar_nombre_nodo()

        self.nodos[nombre] = (x_limitado, y_limitado)
        self.contador_nodos += 1
        return nombre

    def eliminar_nodo(self, nombre):
        if nombre in self.nodos:
            del self.nodos[nombre]
            self.arcos = [
                (u, v, w)
                for u, v, w in self.arcos
                if u != nombre and v != nombre
            ]

    def agregar_arco(self, u, v, peso):
        if not self.existe_arco(u, v) and u != v:
            self.arcos.append((u, v, float(peso)))

    def eliminar_arco(self, arco):
        if arco in self.arcos:
            self.arcos.remove(arco)

    def existe_arco(self, u, v):
        for n1, n2, _ in self.arcos:
            if (n1 == u and n2 == v) or (n1 == v and n2 == u):
                return True
        return False

    def obtener_nodo_en_posicion(self, x, y, radio=22):
        for nombre, (nx, ny) in self.nodos.items():
            if math.hypot(x - nx, y - ny) <= radio:
                return nombre
        return None

    def obtener_arco_en_posicion(self, x, y, umbral=15):
        for u, v, w in self.arcos:
            x1, y1 = self.nodos[u]
            x2, y2 = self.nodos[v]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if math.hypot(x - mx, y - my) <= umbral:
                return (u, v, w)
        return None

    def es_red_conexa(self):
        if not self.nodos:
            return False, "La red no contiene ningún nodo."

        nodos_lista = list(self.nodos.keys())
        if len(nodos_lista) == 1:
            return True, "OK"

        adj = {u: [] for u in self.nodos}
        for u, v, _ in self.arcos:
            adj[u].append(v)
            adj[v].append(u)

        inicio = nodos_lista[0]
        visitados = set([inicio])
        cola = [inicio]

        while cola:
            actual = cola.pop(0)
            for vecino in adj[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        if len(visitados) == len(self.nodos):
            return True, "OK"
        return (
            False,
            f"La red NO es conexa. Solo se alcanzaron {len(visitados)} de"
            f" {len(self.nodos)} nodos.",
        )

    def generar_red_aleatoria(self, cant_nodos, ancho_canvas, alto_canvas):
        self.nodos = {}
        self.arcos = []
        self.contador_nodos = 0

        nombres_nodos = []
        for _ in range(cant_nodos):
            nombre = self.agregar_nodo(
                random.randint(80, max(100, ancho_canvas - 100)),
                random.randint(80, max(100, alto_canvas - 100)),
            )
            nombres_nodos.append(nombre)

        for i in range(1, cant_nodos):
            u = nombres_nodos[i]
            v = random.choice(nombres_nodos[:i])
            peso = round(random.uniform(1.0, 20.0), 2)
            self.agregar_arco(u, v, peso)

        arcos_extra = random.randint(2, cant_nodos)
        for _ in range(arcos_extra):
            u, v = random.sample(nombres_nodos, 2)
            if not self.existe_arco(u, v):
                peso = round(random.uniform(1.0, 25.0), 2)
                self.agregar_arco(u, v, peso)

    def obtener_aristas_de_nodo(self, nodo_id):
        """Devuelve todos los arcos conectados a un nodo específico (u, v,

        w).
        """
        res = []
        for u, v, w in self.arcos:
            if u == nodo_id or v == nodo_id:
                res.append((u, v, w))
        return res

    def obtener_arista_entre(self, id1, id2):
        """Devuelve el arco que conecta dos nodos por sus IDs."""
        for u, v, w in self.arcos:
            if (u == id1 and v == id2) or (u == id2 and v == id1):
                return (u, v, w)
        return None