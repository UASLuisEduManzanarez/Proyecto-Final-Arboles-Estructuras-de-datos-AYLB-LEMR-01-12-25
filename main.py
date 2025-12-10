import os
import sys
from SistemaArchivos9 import SistemaArchivos

# Colores para la consola (opcional, funcionará en la mayoría de terminales)
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_ayuda():
    print(f"""
    {BOLD}--- COMANDOS DISPONIBLES ---{RESET}
    {GREEN}ls{RESET}              : Listar hijos de la carpeta actual
    {GREEN}mkdir{RESET} <nombre> : Crear nueva carpeta (pide ID después)
    {GREEN}touch{RESET} <nombre> : Crear nuevo archivo (pide ID después)
    {GREEN}cd{RESET} <id>         : Navegar a una carpeta (usar '..' para subir, '0' para raíz)
    {GREEN}mv{RESET}              : Mover un nodo (sigue las instrucciones)
    {GREEN}rn{RESET}              : Renombrar un nodo
    {GREEN}rm{RESET} <id>         : Eliminar nodo (enviar a papelera)
    {GREEN}search{RESET} <prefijo>: Buscar archivos por nombre
    {GREEN}tree{RESET}            : Ver todo el árbol
    {GREEN}preorden{RESET}        : Exportar recorrido preorden
    {GREEN}papelera{RESET}        : Ver/Vaciar papelera
    {GREEN}save{RESET}            : Guardar cambios en JSON
    {GREEN}exit{RESET}            : Salir
    """)

def main():
    sistema = SistemaArchivos()
    sistema.cargar_json()
    
    # Control de navegación (Empezamos en la raíz)
    nodo_actual = sistema.raiz

    limpiar_pantalla()
    print(f"{BOLD}Bienvenido al Sistema de Archivos (Proyecto Estructuras){RESET}")
    print("Escribe 'help' para ver los comandos.")

    while True:
        # Prompt estilo terminal: usuario@sistema:/ruta/actual $
        ruta_visual = f"/{nodo_actual.nombre}" if nodo_actual.id != "0" else "/"
        entrada = input(f"\n{BLUE}user@fs:{ruta_visual} ({nodo_actual.id}) ${RESET} ").strip().split()
        
        if not entrada: continue
        comando = entrada[0].lower()
        argumento = entrada[1] if len(entrada) > 1 else None

        # --- COMANDOS BÁSICOS ---
        if comando == "exit":
            sistema.guardar_json()
            print("👋 Cambios guardados. ¡Adiós!")
            break
            
        elif comando == "help":
            imprimir_ayuda()

        elif comando == "save":
            ok, msg = sistema.guardar_json()
            print(msg)

        # --- NAVEGACIÓN Y LISTADO ---
        elif comando == "ls":
            print(f"{BOLD}Contenido de '{nodo_actual.nombre}':{RESET}")
            if not nodo_actual.hijos:
                print("  (vacío)")
            for hijo in nodo_actual.hijos:
                icono = "📁" if hijo.tipo == "carpeta" else "📄"
                print(f"  {icono} {hijo.nombre} \t[ID: {hijo.id}]")

        elif comando == "tree":
            # Función auxiliar visual
            def mostrar(nodo, nivel):
                indent = "    " * nivel
                icono = "📁" if nodo.tipo == "carpeta" else "📄"
                print(f"{indent}{icono} {nodo.nombre} ({nodo.id})")
                for h in nodo.hijos: mostrar(h, nivel + 1)
            mostrar(sistema.raiz, 0)

        elif comando == "cd":
            if not argumento:
                print("Uso: cd <id_carpeta> (o '0' para raíz)")
                continue
            
            if argumento == "0":
                nodo_actual = sistema.raiz
            elif argumento == "..":
                # Ir al padre
                padre = sistema._buscar_padre(nodo_actual.id, sistema.raiz)
                if padre: nodo_actual = padre
            else:
                destino = sistema.buscar_nodo(argumento)
                if destino and destino.tipo == "carpeta":
                    nodo_actual = destino
                else:
                    print(f"{RED}Error: ID no encontrado o no es carpeta.{RESET}")

        # --- CREACIÓN ---
        elif comando in ["mkdir", "touch"]:
            if not argumento:
                print(f"Uso: {comando} <nombre>")
                continue
            
            nuevo_id = input("   Ingrese ID único para el nuevo nodo: ").strip()
            tipo = "carpeta" if comando == "mkdir" else "archivo"
            contenido = None
            if tipo == "archivo":
                contenido = input("   Contenido del archivo: ")
            
            ok, msg = sistema.crear_nodo(nodo_actual.id, nuevo_id, argumento, tipo, contenido)
            print(f"{GREEN if ok else RED}{msg}{RESET}")

        # --- EDICIÓN (RENAME / MOVE) ---
        elif comando == "rn": # Rename
            target_id = input("   ID del nodo a renombrar: ")
            nuevo_nombre = input("   Nuevo nombre: ")
            ok, msg = sistema.renombrar_nodo(target_id, nuevo_nombre)
            print(f"{GREEN if ok else RED}{msg}{RESET}")

        elif comando == "mv": # Move
            nodo_id = input("   ID del nodo a mover: ")
            destino_id = input("   ID de la carpeta destino: ")
            ok, msg = sistema.mover_nodo(nodo_id, destino_id)
            print(f"{GREEN if ok else RED}{msg}{RESET}")

        # --- ELIMINACIÓN Y PAPELERA ---
        elif comando == "rm":
            if not argumento:
                print("Uso: rm <id>")
                continue
            ok, msg = sistema.eliminar_nodo(argumento)
            print(f"{GREEN if ok else RED}{msg}{RESET}")

        elif comando == "papelera":
            print(f"{BOLD}--- PAPELERA DE RECICLAJE ---{RESET}")
            print(sistema.ver_papelera())
            opcion = input("¿Vaciar papelera? (s/n): ").lower()
            if opcion == 's':
                print(sistema.vaciar_papelera())

        # --- BÚSQUEDA Y EXPORTACIÓN ---
        elif comando == "search":
            if not argumento:
                print("Uso: search <prefijo>")
                continue
            resultados = sistema.buscar_autocompletado(argumento)
            print(f"Resultados para '{argumento}':")
            for res in resultados:
                print(f"  * {res['nombre']} (IDs: {res['ids']})")

        elif comando == "preorden":
            print(f"{BOLD}--- RECORRIDO PREORDEN ---{RESET}")
            print(sistema.exportar_preorden())

        else:
            print("Comando no reconocido. Escribe 'help'.")

if __name__ == "__main__": main()