# Proyecto de Análisis de Redes Viales

Este proyecto implementa distintas representaciones de grafos y algoritmos de análisis sobre una red vial obtenida a partir de datos geográficos.

## Autores

- Mauricio Andre Garron Claros
- Huascar Rivero Escobar

## Requisitos

* Python 3.13+

## Configuración del entorno

Se recomienda utilizar un entorno virtual.

### Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## Datasets

Los archivos de entrada se encuentran en el directorio `datasets/`.

* `nodes.csv`: nodos de la red vial.
* `edges.csv`: aristas originales.
* `edges-clean.csv`: aristas procesadas y utilizadas por los algoritmos.

## Limpieza de datos

La lógica de limpieza y preparación de los datos se encuentra documentada e implementada en el archivo:

```text
data-cleansing.ipynb
```

Ese módulo contiene el proceso detallado de transformación de los datos originales hacia los archivos utilizados por los algoritmos del proyecto.

## Ejecución

Los distintos análisis se ejecutan desde `main.py` mediante argumentos de línea de comandos.

Formato general:

```bash
python main.py <opcion>
```

## Comandos disponibles

### Generar grafo serializado

Construye un grafo a partir de `edges-clean.csv` y lo almacena en formato pickle para reutilizarlo posteriormente.

```bash
python main.py make_graph
```

Genera el archivo:

```text
adj-ls-dist-nodir.pkl
```

Este archivo representa un grafo de lista de adyacencia no dirigido con pesos basados en distancia en metros.

---

### Alcance vehicular

Calcula todos los nodos alcanzables desde un nodo origen dentro de una distancia máxima.

```bash
python main.py vehicle_range
```

Parámetros actualmente configurados en el código:

* Nodo origen: `0`
* Distancia máxima: `5000 m`
* Representación: lista de adyacencia

---

### Islas viales

Analiza las componentes conexas débiles de la red vial.

```bash
python main.py vial_islands
```

Requiere haber generado previamente: `adj-ls-dist-nodir.pkl`

```bash
python main.py make_graph
```

---

### Diámetro vial

Calcula el diámetro de la red vial.

```bash
python main.py diameter
```

Utiliza los archivos:

```text
datasets/nodes.csv
datasets/edges.csv
```

---

### Árbol de expansión mínima (MST)

Calcula un árbol de expansión mínima sobre la componente gigante de la red, obtenida de las **Islas Viales**.

```bash
python main.py vial_mst
```

Requiere haber generado previamente: `adj-ls-dist-nodir.pkl`

```bash
python main.py make_graph
```

El procedimiento:

1. Carga el grafo serializado.
2. Identifica la componente gigante por medio de Islas Viales.
3. Calcula el MST sobre dicha componente.

## Flujo recomendado

1. Procesar y limpiar los datos utilizando la lógica descrita en `data-cleansing`.
2. Generar el grafo serializado:

```bash
python main.py make_graph
```

3. Ejecutar cualquiera de los análisis:

```bash
python main.py vial_islands
python main.py vial_mst
python main.py vehicle_range
python main.py diameter
```
