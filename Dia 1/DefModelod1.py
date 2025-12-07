import json
import os
import uuid # Para generar IDs únicos automáticamente

class Node:
    """Representa un archivo o una carpeta en la jerarquía."""

    def _init_(self, name, node_type, content=None, parent=None):
        # Especificaciones del modelo de nodo 
        self.id = str(uuid.uuid4())
        self.nombre = name
        self.tipo = node_type # 'carpeta' o 'archivo' 
        self.contenido = content # Solo valor si es 'archivo' 
        self.children = [] # Lista de nodos hijos 
        self.parent = parent # Referencia al nodo padre (útil para la ruta)
    
    def _repr_(self):
        """Representación simple del nodo para impresión."""
        return f"({self.tipo}: {self.nombre} [ID: {self.id}])"
    
    def to_dict(self):
        """Convierte el nodo y sus hijos a un diccionario serializable."""
        node_dict = {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "children": [child.to_dict() for child in self.children]
        }
        return node_dict