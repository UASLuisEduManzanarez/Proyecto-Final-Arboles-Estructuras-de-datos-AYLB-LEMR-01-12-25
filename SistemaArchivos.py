from ModeloDia1 import Nodo

class SistemaArchivos:
    def __init__(self):
        # Inicializamos con la raíz según tu JSON
        self.raiz = Nodo("0", "raíz", "carpeta", None)

    def buscar_nodo(self, id_objetivo, nodo_actual=None):
        """Busca un nodo por su ID recursivamente."""
        if nodo_actual is None:
            nodo_actual = self.raiz
        
        # Caso base: encontramos el nodo
        if nodo_actual.id == id_objetivo:
            return nodo_actual
        
        # Búsqueda recursiva en los hijos
        for hijo in nodo_actual.hijos:
            resultado = self.buscar_nodo(id_objetivo, hijo)
            if resultado:
                return resultado
        return None

    def crear_nodo(self, id_padre, id_nuevo, nombre, tipo, contenido=None):
        """Crea un nuevo nodo y lo agrega a un padre existente."""
        padre = self.buscar_nodo(id_padre)
        if not padre:
            print(f"Error: Padre con id {id_padre} no encontrado.")
            return False
        
        if padre.tipo != "carpeta":
            print(f"Error: No se pueden agregar hijos a un archivo ({padre.nombre}).")
            return False

        nuevo_nodo = Nodo(id_nuevo, nombre, tipo, contenido)
        padre.hijos.append(nuevo_nodo)
        print(f"Creado: {nombre} (ID: {id_nuevo}) dentro de {padre.nombre}")
        return True

    def eliminar_nodo(self, id_nodo):
        """Elimina un nodo buscando a su padre (no se puede eliminar raíz)."""
        if id_nodo == self.raiz.id:
            print("Error: No se puede eliminar la raíz.")
            return False
        
        # Función auxiliar para encontrar al padre
        padre = self._buscar_padre(id_nodo, self.raiz)
        if padre:
            for hijo in padre.hijos:
                if hijo.id == id_nodo:
                    padre.hijos.remove(hijo)
                    print(f"Eliminado nodo ID: {id_nodo}")
                    return True
        print("Error: Nodo no encontrado.")
        return False

    def _buscar_padre(self, id_hijo, nodo_actual):
        """Auxiliar para encontrar el padre de un nodo."""
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            # Recursión
            resultado = self._buscar_padre(id_hijo, hijo)
            if resultado:
                return resultado
        return None

    def mostrar_arbol(self, nodo=None, nivel=0):
        """Imprime la estructura visualmente (Preorden visual)."""
        if nodo is None:
            nodo = self.raiz
        
        indentacion = "  " * nivel
        icono = "📁" if nodo.tipo == "carpeta" else "📄"
        print(f"{indentacion}{icono} {nodo.nombre} (ID: {nodo.id})")
        
        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)