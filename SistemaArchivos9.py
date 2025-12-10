import json
import os
from ModeloDia4 import Nodo
from trie import Trie

class SistemaArchivos:
    def _init_(self):
        self.raiz = Nodo("0", "raíz", "carpeta", None)
        self.archivo_bd = "filesystem.json"
        self.indice = Trie()
        # Nueva lista para la papelera (Día 7-9) 
        self.papelera = [] 

    # --- MÉTODOS DE NAVEGACIÓN Y BÚSQUEDA ---
    
    def buscar_nodo(self, id_objetivo, nodo_actual=None):
        if nodo_actual is None: nodo_actual = self.raiz
        if nodo_actual.id == id_objetivo: return nodo_actual
        for hijo in nodo_actual.hijos:
            res = self.buscar_nodo(id_objetivo, hijo)
            if res: return res
        return None

    def _buscar_padre(self, id_hijo, nodo_actual):
        """Encuentra al padre de un nodo dado."""
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            res = self._buscar_padre(id_hijo, hijo)
            if res: return res
        return None

    def buscar_autocompletado(self, prefijo):
        return self.indice.buscar_por_prefijo(prefijo)

    # --- OPERACIONES DEL ÁRBOL (CRUD + MOVIMIENTOS) ---

    def crear_nodo(self, id_padre, id_nuevo, nombre, tipo, contenido=None):
        padre = self.buscar_nodo(id_padre)
        if not padre: return False, "Padre no encontrado."
        if padre.tipo != "carpeta": return False, "El padre no es una carpeta."
        
        # Validar ID único
        if self.buscar_nodo(id_nuevo): return False, "ID ya existe."

        nuevo = Nodo(id_nuevo, nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        self.indice.insertar(nombre, id_nuevo) # Actualizar Trie
        return True, f"Nodo '{nombre}' creado exitosamente."

    def eliminar_nodo(self, id_nodo):
        """Mueve el nodo a la papelera en lugar de borrarlo permanentemente."""
        if id_nodo == self.raiz.id: return False, "No se puede eliminar la raíz."
        
        padre = self._buscar_padre(id_nodo, self.raiz)
        if not padre: return False, "Nodo no encontrado."

        for i, hijo in enumerate(padre.hijos):
            if hijo.id == id_nodo:
                nodo_a_borrar = padre.hijos.pop(i)
                # Agregar a la papelera (Día 7-9: Papelera temporal )
                self.papelera.append(nodo_a_borrar)
                # Nota: No borramos del Trie aún para permitir recuperación,
                # o podríamos borrarlo y re-insertarlo al restaurar.
                # Por consistencia, reconstruiremos el índice al final.
                self.reconstruir_indice()
                return True, f"Nodo '{nodo_a_borrar.nombre}' enviado a la papelera."
        return False, "Error desconocido al eliminar."

    def mover_nodo(self, id_nodo, id_nuevo_padre):
        """Mueve un nodo de una carpeta a otra (Día 7-9: Mover nodo )."""
        if id_nodo == self.raiz.id: return False, "No se puede mover la raíz."
        if id_nodo == id_nuevo_padre: return False, "No se puede mover dentro de sí mismo."

        nodo = self.buscar_nodo(id_nodo)
        nuevo_padre = self.buscar_nodo(id_nuevo_padre)
        padre_actual = self._buscar_padre(id_nodo, self.raiz)

        if not nodo: return False, "Nodo origen no existe."
        if not nuevo_padre: return False, "Carpeta destino no existe."
        if not padre_actual: return False, "Error de integridad (sin padre)."
        if nuevo_padre.tipo != "carpeta": return False, "El destino no es una carpeta."

        # Validar que no estemos moviendo una carpeta dentro de uno de sus hijos
        if self._es_descendiente(id_nodo, id_nuevo_padre):
             return False, "No se puede mover una carpeta dentro de sus propios hijos."

        # Realizar el movimiento
        padre_actual.hijos.remove(nodo)
        nuevo_padre.hijos.append(nodo)
        return True, f"Movido '{nodo.nombre}' a '{nuevo_padre.nombre}'."

    def renombrar_nodo(self, id_nodo, nuevo_nombre):
        """Renombra un nodo y actualiza el Trie (Día 7-9: Renombrar )."""
        if id_nodo == self.raiz.id: 
            self.raiz.nombre = nuevo_nombre
            return True, "Raíz renombrada."

        nodo = self.buscar_nodo(id_nodo)
        if not nodo: return False, "Nodo no encontrado."

        nodo.nombre = nuevo_nombre
        self.reconstruir_indice() # Importante actualizar el Trie
        return True, f"Renombrado a '{nuevo_nombre}'."

    def _es_descendiente(self, id_ancestro, id_posible_descendiente):
        """Verifica si el id_posible_descendiente está dentro de id_ancestro."""
        ancestro = self.buscar_nodo(id_ancestro)
        res = self.buscar_nodo(id_posible_descendiente, ancestro)
        return res is not None

    # --- REPORTES Y EXPORTACIÓN ---

    def exportar_preorden(self):
        """Genera una cadena con el recorrido en Preorden (Día 7-9: Exportar )."""
        resultado = []
        self._recorrido_preorden(self.raiz, resultado)
        return "\n".join(resultado)

    def _recorrido_preorden(self, nodo, lista):
        tipo = "(C)" if nodo.tipo == "carpeta" else "(A)"
        lista.append(f"{tipo} {nodo.nombre} [ID: {nodo.id}]")
        for hijo in nodo.hijos:
            self._recorrido_preorden(hijo, lista)

    def ver_papelera(self):
        if not self.papelera: return "Papelera vacía."
        return "\n".join([f"- {n.nombre} ({n.id})" for n in self.papelera])

    def vaciar_papelera(self):
        self.papelera = []
        return "Papelera vaciada."

    # --- PERSISTENCIA Y AUXILIARES ---

    def reconstruir_indice(self):
        self.indice = Trie()
        self._indexar_recursivo(self.raiz)

    def _indexar_recursivo(self, nodo):
        self.indice.insertar(nodo.nombre, nodo.id)
        for hijo in nodo.hijos:
            self._indexar_recursivo(hijo)

    def guardar_json(self):
        datos = self.raiz.to_dict()
        try:
            with open(self.archivo_bd, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True, "Guardado exitoso."
        except Exception as e:
            return False, str(e)

    def cargar_json(self):
        if not os.path.exists(self.archivo_bd): return False
        try:
            with open(self.archivo_bd, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.raiz = Nodo.from_dict(datos)
            self.reconstruir_indice()
            # Nota: La papelera no persiste en el JSON según requerimientos básicos,
            # así que se inicia vacía al cargar.
            self.papelera = [] 
            return True
        except: return False