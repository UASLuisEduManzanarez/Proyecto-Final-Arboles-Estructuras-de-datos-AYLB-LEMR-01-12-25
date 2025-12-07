import json
import os
from ModeloDia4 import Nodo
from trie import Trie  # Importamos la nueva estructura

class SistemaArchivos:
    def __init__(self):
        self.raiz = Nodo("0", "raíz", "carpeta", None)
        self.archivo_bd = "filesystem.json"
        # Inicializamos el Trie para búsquedas
        self.indice = Trie()

    # --- MÉTODOS DE BÚSQUEDA Y TRIE (DÍA 5-6) ---

    def reconstruir_indice(self):
        """
        Borra el índice actual y recorre todo el árbol para
        llenar el Trie nuevamente. Útil tras cargar JSON o eliminar nodos.
        """
        self.indice = Trie() # Reiniciar
        print("🔄 Reconstruyendo índice de búsqueda...")
        self._indexar_recursivo(self.raiz)
    
    def _indexar_recursivo(self, nodo):
        # Insertamos el nombre del nodo actual en el Trie
        self.indice.insertar(nodo.nombre, nodo.id)
        # Recorremos hijos
        for hijo in nodo.hijos:
            self._indexar_recursivo(hijo)

    def buscar_autocompletado(self, prefijo):
        """Busca archivos/carpetas que inicien con el prefijo."""
        resultados = self.indice.buscar_por_prefijo(prefijo)
        print(f"🔎 Resultados para '{prefijo}':")
        for res in resultados:
            print(f"   - {res['nombre']} (IDs: {res['ids']})")
        return resultados

    # --- MÉTODOS DE PERSISTENCIA (DÍA 4) ---

    def guardar_json(self):
        datos = self.raiz.to_dict()
        try:
            with open(self.archivo_bd, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f"💾 Sistema guardado en '{self.archivo_bd}'")
            return True
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False

    def cargar_json(self):
        if not os.path.exists(self.archivo_bd):
            return False
        try:
            with open(self.archivo_bd, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.raiz = Nodo.from_dict(datos)
            print(f"📂 Sistema cargado. Actualizando índice...")
            # IMPORTANTE: Al cargar datos, debemos actualizar el Trie
            self.reconstruir_indice()
            return True
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
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
            print(f"Error: {padre.nombre} no es una carpeta.")
            return
            
        nuevo = Nodo(id_nuevo, nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        
        # IMPORTANTE: Insertar en el Trie al crear
        self.indice.insertar(nombre, id_nuevo)
        print(f"✅ Creado: {nombre}")

    def eliminar_nodo(self, id_nodo):
        """Elimina un nodo y actualiza el Trie."""
        if id_nodo == self.raiz.id:
            print("Error: No se puede eliminar la raíz.")
            return

        padre = self._buscar_padre(id_nodo, self.raiz)
        if padre:
            for i, hijo in enumerate(padre.hijos):
                if hijo.id == id_nodo:
                    eliminado = padre.hijos.pop(i)
                    print(f"🗑️ Eliminado: {eliminado.nombre}")
                    # Reconstruimos el índice para eliminar la referencia del Trie
                    self.reconstruir_indice()
                    return
        print("Error: Nodo no encontrado.")

    def _buscar_padre(self, id_hijo, nodo_actual):
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            res = self._buscar_padre(id_hijo, hijo)
            if res: return res
        return None

    def mostrar_arbol(self, nodo=None, nivel=0):
        if nodo is None: nodo = self.raiz
        indent = "    " * nivel
        icono = "📁" if nodo.tipo == "carpeta" else "📄"
        print(f"{indent}{icono} {nodo.nombre}")
        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)