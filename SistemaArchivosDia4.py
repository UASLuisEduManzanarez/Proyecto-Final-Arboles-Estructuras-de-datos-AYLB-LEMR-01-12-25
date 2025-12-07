import json
import os
from ModeloDia4 import Nodo

class SistemaArchivos:
    def __init__(self):
        # Inicializa con una raíz por defecto, pero idealmente cargará el JSON
        self.raiz = Nodo("0", "raíz", "carpeta", None)
        self.archivo_bd = "filesystem.json" # Nombre del archivo JSON

    # --- MÉTODOS DE PERSISTENCIA (DÍA 4) ---

    def guardar_json(self):
        """Exporta el estado actual del árbol al archivo JSON local."""
        datos = self.raiz.to_dict()
        try:
            with open(self.archivo_bd, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f" Sistema guardado exitosamente en '{self.archivo_bd}'")
            return True
        except Exception as e:
            print(f" Error al guardar: {e}")
            return False

    def cargar_json(self):
        """Carga el árbol desde el archivo JSON, reemplazando el estado actual."""
        if not os.path.exists(self.archivo_bd):
            print(f" Archivo '{self.archivo_bd}' no encontrado. Se inicia con raíz vacía.")
            return False

        try:
            with open(self.archivo_bd, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.raiz = Nodo.from_dict(datos)
            print(f"Sistema cargado correctamente desde '{self.archivo_bd}'")
            return True
        except Exception as e:
            print(f"Error al cargar: {e}")
            return False

    # --- MÉTODOS OPERATIVOS (DÍA 2-3) ---
    
    def buscar_nodo(self, id_objetivo, nodo_actual=None):
        if nodo_actual is None:
            nodo_actual = self.raiz
        if nodo_actual.id == id_objetivo:
            return nodo_actual
        for hijo in nodo_actual.hijos:
            resultado = self.buscar_nodo(id_objetivo, hijo)
            if resultado:
                return resultado
        return None

    def crear_nodo(self, id_padre, id_nuevo, nombre, tipo, contenido=None):
        padre = self.buscar_nodo(id_padre)
        if not padre:
            print(f"Error: Padre {id_padre} no encontrado.")
            return
        if padre.tipo != "carpeta":
            print(f"Error: {padre.nombre} es un archivo, no puede tener hijos.")
            return
            
        nuevo = Nodo(id_nuevo, nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        print(f"Nodo '{nombre}' creado bajo '{padre.nombre}'")

    def mostrar_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        indent = "    " * nivel
        icono = "" if nodo.tipo == "carpeta" else ""
        print(f"{indent}{icono} {nodo.nombre} (ID: {nodo.id})")
        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)