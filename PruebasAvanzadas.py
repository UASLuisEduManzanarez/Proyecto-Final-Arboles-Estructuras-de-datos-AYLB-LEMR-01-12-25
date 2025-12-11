import time
import random
import string
import sys

from SistemadeArchivos9 import SistemaArchivos

# Colores basicos para la consola
RESET = "\033[0m"
VERDE = "\033[92m"
ROJO = "\033[91m"
AZUL = "\033[96m"
NEGRITA = "\033[1m"

def imprimir_titulo(texto):
    print(f"\n{NEGRITA}{'='*50}")
    print(f" {texto}")
    print(f"{'='*50}{RESET}")

# Generador de strings aleatorios para no escribirlos a mano
def generar_id_random():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def generar_nombre_random():
    return ''.join(random.choices(string.ascii_uppercase, k=1)) + \
           ''.join(random.choices(string.ascii_lowercase, k=5))

def prueba_casos_raros(sistema):
    imprimir_titulo("1. PRUEBAS DE CASOS RAROS (A ver si truena)")

    # CASO 1: Intentar borrar la raiz (no deberia dejarnos)
    print(" -> Intentando borrar la carpeta raiz...")
    ok, msg = sistema.eliminar_nodo("0")
    if not ok:
        print(f"{VERDE} [OK] El sistema se defendio bien ({msg}){RESET}")
    else:
        print(f"{ROJO} [FAIL] Dejo borrar la raiz, esto esta mal.{RESET}")

    # CASO 2: Checar si detecta IDs repetidos
    print("\n -> Intentando crear un ID que ya existe...")
    sistema.crear_nodo("0", "test_id", "Carpeta Test", "carpeta")
    # Intentamos crear otro con el mismo ID "test_id"
    ok, msg = sistema.crear_nodo("0", "test_id", "Carpeta Duplicada", "carpeta")
    if not ok:
        print(f"{VERDE} [OK] Detecto el duplicado correctamente ({msg}){RESET}")
    else:
        print(f"{ROJO} [FAIL] Dejo crear duplicados.{RESET}")

    # CASO 3: Ciclos (Mover una carpeta adentro de su propio hijo)
    print("\n -> Intentando mover una carpeta adentro de su propio hijo...")
    sistema.crear_nodo("0", "padre_move", "Padre", "carpeta")
    sistema.crear_nodo("padre_move", "hijo_move", "Hijo", "carpeta")
    
    # Tratamos de mover al Padre adentro del Hijo
    ok, msg = sistema.mover_nodo("padre_move", "hijo_move")
    if not ok:
        print(f"{VERDE} [OK] Evito el ciclo infinito ({msg}){RESET}")
    else:
        print(f"{ROJO} [FAIL] Se rompio la logica del arbol (ciclo creado).{RESET}")

def prueba_carga(sistema):
    imprimir_titulo("2. PRUEBA DE CARGA (Meter muchos datos)")
    
    CANTIDAD = 5000 
    print(f" -> Creando {CANTIDAD} archivos de golpe, espera un poco...")
    
    inicio = time.time()
    
    for i in range(CANTIDAD):
        # Generamos datos de relleno
        id_nuevo = f"auto_{i}"
        nombre = f"Archivo_{i}_{generar_nombre_random()}"
        # Metemos todo en la raiz para hacerlo rapido
        sistema.crear_nodo("0", id_nuevo, nombre, "archivo", "texto de relleno")
        
        # Una barra de carga simple para ver que no se trabo
        if i % 1000 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
            
    fin = time.time()
    tiempo_total = fin - inicio
    print(f"\n\n [TIEMPO] Se tardo: {tiempo_total:.4f} segundos")
    print(f" [VELOCIDAD] Unos {CANTIDAD / tiempo_total:.0f} archivos por segundo")

    # Probamos el Trie (Buscador)
    print(f"\n{AZUL} -> Probando que tan rapido busca (Trie)...{RESET}")
    inicio_busq = time.time()
    # Buscamos algo que sabemos que existe
    resultados = sistema.buscar_autocompletado("Archivo_100")
    fin_busq = time.time()
    
    print(f"Encontro: {len(resultados)} coincidencias")
    print(f" [TIEMPO] Busqueda: {fin_busq - inicio_busq:.6f} segundos")

    # Probamos exportar todo el arbol a texto
    print(f"\n{AZUL} -> Exportando todo el arbol masivo...{RESET}")
    inicio_exp = time.time()
    texto = sistema.exportar_preorden()
    fin_exp = time.time()
    print(f"Tamaño del texto generado: {len(texto)} caracteres")
    print(f" [TIEMPO] Exportacion: {fin_exp - inicio_exp:.4f} segundos")

def main():
    # Usamos una instancia nueva para no modificar el json real
    sistema = SistemaArchivos()
    
    # 1. Corremos las pruebas de casos raros
    prueba_casos_raros(sistema)
    
    # 2. Corremos la prueba de velocidad
    # Reiniciamos la variable para empezar limpio
    sistema = SistemaArchivos() 
    prueba_carga(sistema)
    
    print("\n LISTO. Pruebas terminadas.")
    print(" Nota: No guarde nada en el JSON para no llenar tu disco de basura.")

if __name__ == "__main__":
    main()