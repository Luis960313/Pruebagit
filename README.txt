========================================================================
                      VERSIÓN EN ESPAÑOL / SPANISH
========================================================================
   ÁRBOL DE EXPANSIÓN MÍNIMA (KRUSKAL) Y CAMINOS MÍNIMOS (DIJKSTRA)
========================================================================
Universidad Tecnológica de Pereira (UTP)
Programa de Ingeniería de Sistemas y Computación
Asignatura: Investigación de Operaciones
Docente: Bibiana Patricia Arias Villada
Autor: Luis Quintero


1. DESCRIPCIÓN DEL PROYECTO
------------------------------------------------------------------------
Aplicación interactiva de escritorio construida en Python mediante la librería
Tkinter. Permite diseñar, modificar y analizar libremente redes ponderadas no
dirigidas para resolver dos problemas fundamentales de optimización de redes:
  • Árbol de Expansión Mínima (AEM): Utilizando el Algoritmo de Kruskal.
  • Caminos Mínimos: Determinando la distancia mínima y los recorridos óptimos
    desde un nodo origen hacia todos los nodos de la red con el Algoritmo de Dijkstra.


2. REQUISITOS DEL SISTEMA
------------------------------------------------------------------------
- Python 3.8 o superior.
- Librería Tkinter (incluida por defecto en la instalación estándar de Python).

* Nota para usuarios de Linux: Si Tkinter no está presente, instálalo vía consola:
  sudo apt-get install python3-tk


3. ESTRUCTURA DEL PROYECTO
------------------------------------------------------------------------
- main.py          : Punto de entrada principal de la aplicación.
- interfaz.py      : Administración de la ventana principal (GUI), eventos del mouse,
                     selección interactiva de origen y ventanas emergentes de reporte.
- grafo.py         : Modelo de datos de la red (Nodos, Arcos, posiciones), control
                     de límites en lienzo, generador alfabético (A, B, C...) y comprobaciones de conexidad.
- kruskal.py       : Algoritmo de Kruskal con estructura Disjoint-Set (Union-Find)
                     e identificación de alternativas/ciclos.
- dijkstra.py      : Algoritmo de Dijkstra para rutas de costo mínimo, reconstrucción de
                     recorridos y validación de pesos no negativos.
- visualizacion.py : Renderizado gráfico en Canvas (colores de estados, nodos con etiquetas
                     flotantes de distancia d[v], resaltado de rutas y arcos).
- exportacion.py   : Módulo de exportación para guardar capturas gráficas (.ps) e informes
                     completos en formato texto (.txt) con validación de red no vacía.


4. INSTRUCCIONES DE EJECUCIÓN
------------------------------------------------------------------------
1. Abre una terminal o consola de comandos en la carpeta raíz del proyecto.
2. Ejecuta el siguiente comando:

   python main.py
   (o en sistemas Linux/macOS: python3 main.py)


5. USO Y FUNCIONALIDADES DE LA APLICACIÓN
------------------------------------------------------------------------
- ➕ Agregar Nodo   : Haz clic en cualquier área del lienzo para colocar un nodo con
                      nombre secuencial alfabético (A, B, C... Z, AA...).
- 🔗 Crear Arco     : Haz clic en dos nodos para unirlos e ingresa su peso.
                      (Si haces clic sobre el peso de un arco existente, podrás editarlo).
- ✋ Mover Nodo     : Arrastra cualquier nodo libremente respetando los límites del lienzo.
- 🗑️ Eliminar       : Haz clic sobre un nodo o arco para eliminarlo de la red.
- 🎲 Red Aleatoria  : Genera automáticamente un grafo de prueba conexo (de 4 a 12 nodos).
- ⚡ Kruskal Directo : Ejecuta Kruskal y resalta en verde los arcos que forman el AEM.
- ▶️ AEM Paso a Paso : Animación interactiva de toma de decisiones (Evaluación, Aceptación y Ciclos).
- 🚩 Dijkstra (Origen): Selecciona este modo y luego haz clic directo con el mouse sobre
                      el NODO ORIGEN. El programa mostrará las etiquetas d[v], la ruta en
                      morado y desplegará una tabla formal estructurada con los recorridos.
- 🔄 Reiniciar      : Borra completamente la red y restablece la interfaz.
- 🖼️ Exportar Imagen: Guarda una imagen (.ps) del Canvas actual (requiere nodos en pantalla).
- 📄 Exportar (.TXT): Genera un reporte detallado con la estructura del grafo, el AEM
                      de Kruskal y la tabla de rutas de Dijkstra.


========================================================================
                  ENGLISH VERSION / VERSIÓN EN INGLÉS
========================================================================
   MINIMUM SPANNING TREE (KRUSKAL) & SHORTEST PATHS (DIJKSTRA)
========================================================================
Course: Operations Research
Instructor: Bibiana Patricia Arias Villada
Author: Luis Quintero


1. PROJECT DESCRIPTION
------------------------------------------------------------------------
An interactive desktop application built in Python using Tkinter. It allows
users to design, edit, and analyze undirected weighted networks to solve two
fundamental network optimization problems:
  • Minimum Spanning Tree (MST): Using Kruskal's Algorithm.
  • Shortest Paths: Determining minimal distances and optimal routes from
    a designated source node to all other reachable nodes using Dijkstra's Algorithm.


2. SYSTEM REQUIREMENTS
------------------------------------------------------------------------
- Python 3.8 or higher.
- Tkinter library (included by default in standard Python installations).

* Note for Linux users: If Tkinter is missing, install it via terminal:
  sudo apt-get install python3-tk


3. PROJECT ARCHITECTURE
------------------------------------------------------------------------
- main.py          : Application entry point.
- interfaz.py      : GUI management, button events, mouse-driven source selection,
                     and structured result modal windows.
- grafo.py         : Graph data model (Nodes, Edges, coordinates), canvas bounds,
                     alphabetical node label generator (A, B, C...), and BFS connectivity check.
- kruskal.py       : Kruskal's algorithm with Union-Find and cycle detection logic.
- dijkstra.py      : Dijkstra's algorithm for shortest path calculation, path reconstruction,
                     and non-negative weight validation.
- visualizacion.py : Canvas rendering functions (color codes, node distance tags d[v],
                     path highlighting, and edge weight rendering).
- exportacion.py   : File export handlers for PostScript images (.ps) and text reports (.txt)
                     including non-empty network validations.


4. INSTALLATION & EXECUTION
------------------------------------------------------------------------
1. Open a terminal or command prompt in the project folder.
2. Run the following command:

   python main.py
   (or on Linux/macOS: python3 main.py)


5. HOW TO USE
------------------------------------------------------------------------
- ➕ Add Node      : Click on the canvas to place nodes labeled alphabetically (A, B, C...).
- 🔗 Create Edge    : Click two nodes to connect them with a weighted edge.
                     (Click the weight tag of an existing edge to modify its value).
- ✋ Move Node      : Drag any node across the canvas within visible boundaries.
- 🗑️ Delete         : Click a node or edge to remove it from the graph.
- 🎲 Random Graph   : Generates a connected random test graph (4 to 12 nodes).
- ⚡ Compute MST    : Direct Kruskal execution highlighting the MST in green.
- ▶️ Step by Step   : Real-time decision trace (Yellow = Testing, Green = Accepted, Red = Cycle).
- 🚩 Select Source  : Enable Dijkstra mode and click directly on any node to select it
                     as the SOURCE. Displays floating d[v] tags, highlights paths in purple,
                     and shows an organized route table.
- 🔄 Reset Network  : Clears the canvas to start a new network from scratch.
- 🖼️️ Export Image   : Saves a PostScript screenshot (.ps) of the canvas (validates non-empty graph).
- 📄 Export (.TXT)  : Generates a comprehensive report with network structure, Kruskal's MST,
                     and Dijkstra's distance/path results.
========================================================================
