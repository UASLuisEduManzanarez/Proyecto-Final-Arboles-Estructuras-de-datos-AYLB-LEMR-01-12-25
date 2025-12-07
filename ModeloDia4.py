import json

class Nodo:
    def __init__(self, id_nodo, nombre, tipo, contenido=None):
        """
        Inicializa un nodo del sistema de archivos.
        """
        self.id = id_nodo
        self.nombre = nombre
        self.tipo = tipo  # "carpeta" o "archivo"
        self.contenido = contenido
        self.hijos = []   # Lista de nodos hijos

    def to_dict(self):
        """
        Convierte el nodo y toda su descendencia a un diccionario
        compatible con el formato JSON requerido.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            # Se llama recursivamente a to_dict para cada hijo
            "children": [hijo.to_dict() for hijo in self.hijos]
        }

    @staticmethod
    def from_dict(data):
        """
        Construye un objeto Nodo (y toda su jerarquía) a partir de un diccionario.
        """
        # Crear el nodo actual
        nodo = Nodo(
            id_nodo=data["id"], 
            nombre=data["nombre"], 
            tipo=data["tipo"], 
            contenido=data.get("contenido") # .get por si viene null
        )
        
        # Si tiene hijos en el JSON, reconstruirlos recursivamente
        if "children" in data:
            for hijo_data in data["children"]:
                nodo_hijo = Nodo.from_dict(hijo_data)
                nodo.hijos.append(nodo_hijo)
                
        return nodo

    def __repr__(self):
        return f"Nodo({self.id}, {self.nombre}, {self.tipo})"