class NodoTrie:
    def __init__(self):
        # Diccionario que mapea caracteres a otros nodos hijos
        self.hijos = {}
        # Indica si en este nodo termina una palabra completa
        self.es_final_palabra = False
        # Lista de IDs de archivos que tienen este nombre
        self.ids_asociados = []

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra, id_nodo):
        """Inserta una palabra en el Trie asociada a un ID de nodo."""
        nodo = self.raiz
        # Convertimos a minúsculas para búsqueda insensible a mayúsculas
        palabra = palabra.lower()
        
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = NodoTrie()
            nodo = nodo.hijos[letra]
        
        nodo.es_final_palabra = True
        nodo.ids_asociados.append(id_nodo)

    def buscar_por_prefijo(self, prefijo):
        """
        Retorna una lista de tuplas (nombre, lista_ids) que coinciden
        con el prefijo dado.
        """
        nodo = self.raiz
        prefijo = prefijo.lower()
        
        # 1. Navegar hasta el final del prefijo
        for letra in prefijo:
            if letra not in nodo.hijos:
                return [] # No hay coincidencias
            nodo = nodo.hijos[letra]
        
        # 2. Recolectar todas las palabras completas a partir de aquí
        resultados = []
        self._recolectar_palabras(nodo, prefijo, resultados)
        return resultados

    def _recolectar_palabras(self, nodo, palabra_actual, resultados):
        """Función recursiva para encontrar todas las palabras bajo un nodo."""
        if nodo.es_final_palabra:
            resultados.append({
                "nombre": palabra_actual,
                "ids": nodo.ids_asociados
            })
        
        for letra, nodo_hijo in nodo.hijos.items():
            self._recolectar_palabras(nodo_hijo, palabra_actual + letra, resultados)