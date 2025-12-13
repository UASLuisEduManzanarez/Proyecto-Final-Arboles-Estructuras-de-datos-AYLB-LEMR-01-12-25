# Proyecto-Final-Arboles-Estructuras-de-datos-AYLB-LEMR-01-12-25
Repositorio de proyecto final de Estructura de Datos

PASO 1: Descripción del Proyecto
El presente proyecto consiste en el diseño e implementación de una simulación de consola para un sistema de archivos, análogo a las interfaces de línea de comandos presentes en sistemas operativos como Linux o Windows.
El núcleo del desarrollo se centra en la aplicación de estructuras de datos no lineales para gestionar la información. A diferencia de los enfoques tradicionales basados en listas lineales o bases de datos relacionales, este sistema implementa una arquitectura basada en Árboles Generales (N-arios) para la gestión de directorios y Trie (Árbol Prefijo) para la optimización de búsquedas y autocompletado. El resultado es un sistema eficiente capaz de organizar, manipular y recuperar información jerárquica con alta performancia.

PASO 2: Requisitos de Ejecución e Instalación
El sistema ha sido desarrollado en el lenguaje de programación Python, lo que garantiza portabilidad y facilidad de ejecución sin dependencias externas complejas.

Procedimiento de Despliegue:
1. Asegurar la instalación del intérprete Python (versión 3.x) en el entorno de host.
2. Desplegar el directorio del proyecto en el sistema local.
3. Iniciar la interfaz de consola ejecutando el script principal desde la terminal:
4. Tras la inicialización, el sistema presentará el prompt de usuario (user@fs:/ $), indicando que se encuentra operativo y listo para recibir instrucciones.

PASO 3: Manual de Operación y Comandos
La interacción con el sistema se realiza mediante una interfaz de línea de comandos (CLI). A continuación, se detallan las operaciones disponibles clasificadas por funcionalidad:

3.1 Navegación y Visualización

ls: Lista los nodos hijos (archivos y carpetas) contenidos en el directorio actual.
tree: Genera y visualiza la estructura jerárquica completa del sistema de archivos, permitiendo una inspección global de la topología del árbol.

3.2 Gestión de Nodos (Creación y Edición)

mkdir <nombre>: Inicializa un nuevo directorio. El sistema solicitará posteriormente la asignación de un ID único.
touch <nombre>: Genera un nuevo archivo. Requiere la asignación de un ID y la introducción del contenido textual asociado.
rn: Permite la modificación del atributo nombre de un nodo existente, actualizando simultáneamente los índices de búsqueda.

3.3 Organización y Eliminación

mv: Traslada un nodo (archivo o carpeta) hacia un directorio destino diferente.
Integridad Referencial: El algoritmo incluye validaciones para impedir movimientos cíclicos (mover una carpeta dentro de sus propios descendientes), preservando la consistencia del árbol.
rm <id>: Ejecuta la eliminación lógica de un nodo.

Gestión de Papelera: Los nodos eliminados son trasladados a una estructura temporal (Papelera de Reciclaje), permitiendo su recuperación o eliminación definitiva posteriormente.

papelera: Visualiza los elementos eliminados lógicamente. Ofrece la opción de vaciado para la eliminación física permanente.

3.4 Búsqueda y Persistencia
search <prefijo>: Ejecuta una búsqueda eficiente por prefijo. Utilizando la estructura Trie, el sistema recupera instantáneamente todas las coincidencias lexicográficas (autocompletado) asociadas al texto ingresado.

save: Serializa el estado actual del árbol y lo almacena en un archivo local con formato JSON, garantizando la persistencia de los datos entre sesiones.
preorden: Exporta el recorrido del árbol utilizando el algoritmo de búsqueda en profundidad (Preorden), útil para análisis estructural y depuración.

4. Arquitectura del Sistema
La implementación técnica se fundamenta en tres pilares teóricos principales para cumplir con los requisitos de eficiencia y escalabilidad:

A. Árbol General (N-ario)
La estructura base del sistema es un Árbol General. Se desestimó el uso de árboles binarios debido a la naturaleza de los sistemas de archivos, donde un directorio puede contener un número arbitrario de subdirectorios y archivos ("hijos"). Cada objeto Nodo mantiene una lista dinámica de referencias a sus nodos hijos, permitiendo una profundidad y amplitud teóricamente infinitas.

B. Optimización mediante Trie (Árbol Prefijo)
Para optimizar la complejidad temporal de las operaciones de búsqueda, se implementó una estructura auxiliar Trie. Cada inserción o modificación de nombre en el árbol principal actualiza este índice. Esto permite que la operación search tenga una complejidad dependiente de la longitud de la palabra buscada, en lugar de depender del número total de archivos en el sistema, logrando tiempos de respuesta óptimos.


C. Persistencia y Serialización
La persistencia de datos se gestiona mediante la serialización de la estructura de objetos a formato JSON. Se implementó un algoritmo recursivo capaz de recorrer la jerarquía del árbol, convirtiendo cada nodo y sus relaciones en un formato de texto estructurado recuperable, asegurando la integridad de los datos al reiniciar la aplicación.

cd <id>: Modifica el directorio de trabajo actual.

Nota: La navegación se basa en el Identificador Único (ID) del nodo para garantizar precisión.

Comandos especiales: cd .. permite ascender al nodo padre; cd 0 retorna a la raíz del sistema.
