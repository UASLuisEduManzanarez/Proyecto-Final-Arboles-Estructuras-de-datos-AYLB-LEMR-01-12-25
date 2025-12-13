# Proyecto-Final-Arboles-Estructuras-de-datos-AYLB-LEMR-01-12-25
Repositorio de proyecto final de Estructura de Datos

1. Descripción del Proyecto
El presente proyecto consiste en el diseño e implementación de una simulación de consola para un sistema de archivos, análogo a las interfaces de línea de comandos presentes en sistemas operativos como Linux o Windows.
El núcleo del desarrollo se centra en la aplicación de estructuras de datos no lineales para gestionar la información. A diferencia de los enfoques tradicionales basados en listas lineales o bases de datos relacionales, este sistema implementa una arquitectura basada en Árboles Generales (N-arios) para la gestión de directorios y Trie (Árbol Prefijo) para la optimización de búsquedas y autocompletado. El resultado es un sistema eficiente capaz de organizar, manipular y recuperar información jerárquica con alta performancia.

2. Requisitos de Ejecución e Instalación
El sistema ha sido desarrollado en el lenguaje de programación Python, lo que garantiza portabilidad y facilidad de ejecución sin dependencias externas complejas.

Procedimiento de Despliegue:
1. Asegurar la instalación del intérprete Python (versión 3.x) en el entorno de host.
2. Desplegar el directorio del proyecto en el sistema local.
3. Iniciar la interfaz de consola ejecutando el script principal desde la terminal:
4. Tras la inicialización, el sistema presentará el prompt de usuario (user@fs:/ $), indicando que se encuentra operativo y listo para recibir instrucciones.

3. Manual de Operación y Comandos
La interacción con el sistema se realiza mediante una interfaz de línea de comandos (CLI). A continuación, se detallan las operaciones disponibles clasificadas por funcionalidad:

3.1 Navegación y Visualización

ls: Lista los nodos hijos (archivos y carpetas) contenidos en el directorio actual.

tree: Genera y visualiza la estructura jerárquica completa del sistema de archivos, permitiendo una inspección global de la topología del árbol.

cd <id>: Modifica el directorio de trabajo actual.

Nota: La navegación se basa en el Identificador Único (ID) del nodo para garantizar precisión.

Comandos especiales: cd .. permite ascender al nodo padre; cd 0 retorna a la raíz del sistema.
