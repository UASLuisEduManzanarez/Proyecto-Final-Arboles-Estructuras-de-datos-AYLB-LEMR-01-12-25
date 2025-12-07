import json

class Nodo:
    def __init__(self, id_nodo, nombre, tipo, contenido=None):
        """
        Inicializa un nodo del sistema de archivos.
        
        :param id_nodo: Identificador único (ej. "0", "file-0203")
        :param nombre: Nombre del archivo o carpeta
        :param tipo: "carpeta" o "archivo"
        :param contenido: Texto del archivo (null/None si es carpeta)
        """
        self.id = id_nodo
        self.nombre = nombre
        self.tipo = tipo  # "carpeta" o "archivo"
        self.contenido = contenido
        self.hijos = []   # Lista de objetos Nodo (children)

    def __repr__(self):
        return f"Nodo({self.id}, {self.nombre}, {self.tipo})"

# --- Bloque de prueba para el Día 1 ---
if __name__ == "__main__":
    # Prueba de creación basada en tu JSON raíz
    raiz = Nodo("0", "raíz", "carpeta", None)
    print(f"Sistema creado: {raiz}")
    print("Estructura definida correctamente.")