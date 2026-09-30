========================================================================
                      VERSIÓN EN ESPAÑOL / SPANISH
========================================================================
   ÁRBOL DE EXPANSIÓN MÍNIMA (AEM) EN PYTHON
========================================================================
Universidad Tecnológica de Pereira (UTP)
Asignatura: Investigación de Operaciones
Docente: Bibiana Patricia Arias Villada
Autor: Luis Quintero


1. DESCRIPCIÓN DEL PROYECTO
------------------------------------------------------------------------
Aplicación interactiva construida en Python con la librería Tkinter que
permite diseñar, editar y analizar redes no dirigidas mediante el algoritmo
de Kruskal para encontrar el Árbol de Expansión Mínima (AEM).

2. REQUISITOS DEL SISTEMA
------------------------------------------------------------------------
- Python 3.8 o superior.
- Librería Tkinter (incluida por defecto en la instalación estándar de Python).

3. ESTRUCTURA DEL PROYECTO
------------------------------------------------------------------------
- main.py          : Punto de entrada principal de la aplicación.
- interfaz.py      : Administración de la ventana, botones y eventos del mouse.
- grafo.py         : Modelo de datos del grafo, límites de pantalla y BFS.
- kruskal.py       : Algoritmo de Kruskal con Union-Find e identificación de empates.
- visualizacion.py   : Lógica de dibujo en Canvas (colores, nodos y aristas).
- exportacion.py     : Funciones para guardar imágenes (.ps) e informes (.txt).

4. INSTRUCCIONES DE EJECUCIÓN
------------------------------------------------------------------------
1. Abre una terminal o consola de comandos en la carpeta del proyecto.
2. Ejecuta el siguiente comando:

   python main.py

5. USO DE LA APLICACIÓN
------------------------------------------------------------------------
- ➕ Agregar Nodo   : Haz clic en el lienzo para crear nodos.
- 🔗 Crear Arco     : Haz clic en dos nodos para unirlos e ingresa su peso.
                      (Si haces clic en el peso de un arco existente, podrás modificarlo).
- ✋ Mover Nodo     : Arrastra cualquier nodo por el lienzo.
- 🗑️ Eliminar       : Haz clic en un nodo o arco para borrarlo.
- ⚡ Calcular AEM    : Ejecuta Kruskal y muestra el árbol sobre la red.
- ▶️ AEM Paso a Paso : Animación detallada decisión por decisión.
- 🎲 Red Aleatoria  : Genera un grafo conexo de prueba automáticamente.
- 🖼️ Exportar       : Opciones para guardar informes en texto e imágenes del AEM.
========================================================================
                  ENGLISH VERSION / VERSIÓN EN INGLÉS
========================================================================
   MINIMUM SPANNING TREE (MST) IN PYTHON
========================================================================
Course: Operations Research
Instructor: Bibiana Patricia Arias Villada
Author: Luis Quintero

1. PROJECT DESCRIPTION
------------------------------------------------------------------------
An interactive desktop application built in Python using Tkinter. It allows
users to design, edit, and analyze undirected weighted graphs to compute 
and visualize the Minimum Spanning Tree (MST) using Kruskal's Algorithm.

2. SYSTEM REQUIREMENTS
------------------------------------------------------------------------
- Python 3.8 or higher.
- Tkinter library (included by default in standard Python installations).

* Note for Linux users: If Tkinter is missing, install it via terminal:
  sudo apt-get install python3-tk

3. PROJECT ARCHITECTURE
------------------------------------------------------------------------
- main.py          : Application entry point.
- interfaz.py      : GUI management, button layout, and event handlers.
- grafo.py         : Graph data structure, screen boundaries, and BFS.
- kruskal.py       : Kruskal's algorithm with Union-Find and tie-break logic.
- visualizacion.py   : Canvas rendering functions (nodes, edges, colors).
- exportacion.py     : File handlers for .txt reports and .ps images.

4. INSTALLATION & EXECUTION
------------------------------------------------------------------------
1. Open a terminal or command prompt in the project folder.
2. Run the following command:

   python main.py

5. HOW TO USE
------------------------------------------------------------------------
- ➕ Add Node   : Click anywhere on the canvas to place a new node.
- 🔗 Create Edge : Click two nodes to connect them with a weighted edge.
                  (Click the weight label of an existing edge to modify it).
- ✋ Move Node   : Drag any node across the screen (bounded within canvas).
- 🗑️ Delete      : Click a node or edge to remove it.
- ⚡ Compute MST : Executes Kruskal directly and highlights the tree paths.
- ▶️ Step by Step: Visual trace showing real-time decisions (Yellow = Testing,
                  Green = Accepted, Red = Cycle).
- 🎲 Random Graph: Generates a fully connected test graph automatically.
- 🖼️ Export MST  : Saves a clean image (.ps) or a detailed report (.txt).
========================================================================
