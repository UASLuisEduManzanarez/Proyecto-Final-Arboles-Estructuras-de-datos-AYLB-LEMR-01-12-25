import json

class Nodo:
    """
    Representa un archivo o una carpeta en la jerarquía del sistema.
    Define el 'Modelo de Nodo' requerido.
    """
    def _init_(self, id_nodo, nombre, es_carpeta=True, contenido=None, padre=None):
        # Campos del Modelo de Nodo
        self.id = id_nodo
        self.nombre = nombre
        self.es_carpeta = es_carpeta  # True si es carpeta, False si es archivo
        self.contenido = contenido    # Contenido del archivo (si aplica)
        self.hijos = []               # Lista de referencias a nodos hijos
        self.padre = padre            # Referencia al nodo padre

    def _repr_(self):
        """Representación legible del nodo para depuración."""
        tipo_str = "DIR" if self.es_carpeta else "FILE"
        return f"[{tipo_str} {self.id}] {self.nombre}"

    # --------------------------------------------------------------------
    # SERIALIZACIÓN (DÍA 1: Definición del Formato JSON)
    # --------------------------------------------------------------------

    def to_dict(self):
        """
        Convierte el nodo y sus hijos a un diccionario serializable que
        cumple con el formato JSON: id, nombre, tipo, contenido, children.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            # Traduce el booleano 'es_carpeta' al string 'tipo' requerido
            "tipo": "carpeta" if self.es_carpeta else "archivo",
            "contenido": self.contenido,
            # Recursividad: llama a to_dict() para cada hijo.
            "children": [hijo.to_dict() for hijo in self.hijos]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Método de clase que construye un objeto Nodo (y sus hijos)
        a partir de un diccionario (cargado desde el JSON).
        """
        es_carpeta = (data["tipo"] == "carpeta")
        
        # Crea el nodo base
        nodo = cls(data["id"], data["nombre"], es_carpeta, data.get("contenido")) 
        
        # Reconstrucción recursiva de los hijos
        if "children" in data:
            for hijo_data in data["children"]:
                hijo_nodo = cls.from_dict(hijo_data)
                hijo_nodo.padre = nodo  # Asigna la referencia al padre
                nodo.hijos.append(hijo_nodo)
                
        return nodo