"""
Script completo para eliminar recursión por izquierda (Algoritmo del libro de Aho)
Incluye toda la lógica del algoritmo sin dependencias externas.

Puedes usarlo de dos formas:
1. python run_prueba.py "A -> Aa | b"
2. python run_prueba.py (te pregunta interactivamente)
"""
import sys
import io


def leer_entrada():
    """
    Lee la entrada del programa y retorna una lista de gramáticas.
    Cada gramática es un diccionario donde las llaves son no terminales
    y los valores son listas de producciones (cada producción es una lista de símbolos).
    """
    n = int(input())
    gramaticas = []

    for _ in range(n):
        k = int(input())
        gramatica = {}
        no_terminales_orden = []

        for _ in range(k):
            linea = input().strip()
            partes = linea.split(' -> ')
            no_terminal = partes[0]
            producciones_str = partes[1].split()

            producciones = []
            for prod in producciones_str:
                if prod == '|':
                    continue
                producciones.append(list(prod))

            gramatica[no_terminal] = producciones
            no_terminales_orden.append(no_terminal)

        gramaticas.append((gramatica, no_terminales_orden))

    return gramaticas


def tiene_recursion_inmediata(producciones, no_terminal):
    """
    Verifica si un no terminal tiene recursión inmediata por la izquierda.
    Retorna True si alguna producción comienza con el mismo no terminal.
    """
    for prod in producciones:
        if len(prod) > 0 and prod[0] == no_terminal:
            return True
    return False


def eliminar_recursion_inmediata(gramatica, no_terminal, no_terminales_usados):
    """
    Elimina la recursión inmediata por la izquierda de un no terminal.
    Si A -> Aα1 | Aα2 | ... | Aαm | β1 | β2 | ... | βn
    Lo convierte en:
    A -> β1A' | β2A' | ... | βnA'
    A' -> α1A' | α2A' | ... | αmA' | ε
    """
    producciones = gramatica[no_terminal]

    recursivas = []
    no_recursivas = []

    for prod in producciones:
        if len(prod) > 0 and prod[0] == no_terminal:
            recursivas.append(prod[1:])
        else:
            no_recursivas.append(prod)

    if len(recursivas) == 0:
        return

    nuevo_no_terminal = generar_nuevo_no_terminal(no_terminales_usados)
    no_terminales_usados.add(nuevo_no_terminal)

    nuevas_producciones = []
    for prod in no_recursivas:
        nuevas_producciones.append(prod + [nuevo_no_terminal])

    gramatica[no_terminal] = nuevas_producciones

    producciones_nuevo = []
    for prod in recursivas:
        producciones_nuevo.append(prod + [nuevo_no_terminal])
    producciones_nuevo.append(['e'])

    gramatica[nuevo_no_terminal] = producciones_nuevo


def generar_nuevo_no_terminal(usados):
    """
    Genera un nuevo símbolo no terminal que no haya sido usado.
    Usa letras mayúsculas del alfabeto en orden.
    """
    for letra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letra not in usados:
            return letra
    return 'X'


def sustituir_producciones(gramatica, no_terminal_i, no_terminal_j):
    """
    Sustituye las producciones de la forma Ai -> Aj γ
    por Ai -> δ1 γ | δ2 γ | ... | δk γ
    donde Aj -> δ1 | δ2 | ... | δk son todas las producciones de Aj.
    """
    producciones_i = gramatica[no_terminal_i]
    producciones_j = gramatica[no_terminal_j]

    nuevas_producciones = []

    for prod_i in producciones_i:
        if len(prod_i) > 0 and prod_i[0] == no_terminal_j:
            gamma = prod_i[1:]
            for prod_j in producciones_j:
                nuevas_producciones.append(prod_j + gamma)
        else:
            nuevas_producciones.append(prod_i)

    gramatica[no_terminal_i] = nuevas_producciones


def eliminar_recursion_izquierda(gramatica, no_terminales_orden):
    """
    Implementa el algoritmo completo de eliminación de recursión por la izquierda.

    Algoritmo:
    1. Ordenar los no terminales A1, A2, ..., An
    2. Para cada i desde 1 hasta n:
       a. Para cada j desde 1 hasta i-1:
          - Reemplazar cada producción Ai -> Aj γ por las expansiones de Aj
       b. Eliminar recursión inmediata de Ai
    """
    n = len(no_terminales_orden)
    no_terminales_usados = set(no_terminales_orden)

    for i in range(n):
        no_terminal_i = no_terminales_orden[i]

        for j in range(i):
            no_terminal_j = no_terminales_orden[j]
            sustituir_producciones(gramatica, no_terminal_i, no_terminal_j)

        if tiene_recursion_inmediata(gramatica[no_terminal_i], no_terminal_i):
            eliminar_recursion_inmediata(gramatica, no_terminal_i, no_terminales_usados)

    return gramatica


def formatear_salida(gramatica, no_terminales_orden):
    """
    Formatea la gramática resultante para imprimirla según el formato requerido.
    Formato: <no_terminal> -> <prod1> <prod2> ... <prodn>
    """
    resultado = []

    todos_no_terminales = []
    for nt in no_terminales_orden:
        if nt in gramatica:
            todos_no_terminales.append(nt)

    for nt in gramatica:
        if nt not in todos_no_terminales:
            todos_no_terminales.append(nt)

    for no_terminal in todos_no_terminales:
        if no_terminal not in gramatica:
            continue

        producciones = gramatica[no_terminal]
        prods_str = []

        for prod in producciones:
            prods_str.append(''.join(prod))

        linea = f"{no_terminal} -> {' '.join(prods_str)}"
        resultado.append(linea)

    return '\n'.join(resultado)


def ejecutar_algoritmo():
    """
    Función principal que coordina la lectura, procesamiento y salida del programa.
    """
    gramaticas = leer_entrada()

    resultados = []

    for gramatica, no_terminales_orden in gramaticas:
        gramatica_sin_recursion = eliminar_recursion_izquierda(gramatica, no_terminales_orden)
        salida = formatear_salida(gramatica_sin_recursion, no_terminales_orden)
        resultados.append(salida)

    print('\n\n'.join(resultados))


def run_with_grammar(grammar_line):
    """Corre el algoritmo con una gramática dada"""
    # Formato del input que espera el algoritmo:
    # Línea 1: número de gramáticas
    # Línea 2: número de no-terminales
    # Línea 3+: producciones
    test_input = f"""1
1
{grammar_line}"""

    # Redirect stdin
    sys.stdin = io.StringIO(test_input)

    print("=" * 60)
    print("INPUT:")
    print(grammar_line)
    print("=" * 60)
    print("OUTPUT:")
    ejecutar_algoritmo()
    print("=" * 60)


def modo_interactivo():
    """Modo interactivo con opción de procesar múltiples gramáticas"""
    print("=" * 60)
    print("LEFT RECURSION ELIMINATION - Interactive Mode")
    print("=" * 60)
    print("\nEjemplos de input válido:")
    print("  A -> Aa | b")
    print("  S -> Sa | Sb | c")
    print("  E -> E+T | T")
    print()

    while True:
        grammar = input("Ingresa la gramática: ").strip()

        if grammar:
            print()
            # Restaurar stdin para que run_with_grammar funcione
            original_stdin = sys.stdin
            run_with_grammar(grammar)
            sys.stdin = original_stdin

            print()
            continuar = input("¿Quieres procesar otra gramática? (s/n): ").strip().lower()

            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n¡Hasta luego!")
                break
            print()
        else:
            print("No ingresaste nada.")
            continuar = input("¿Quieres intentar de nuevo? (s/n): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n¡Hasta luego!")
                break
            print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo 1: Pasaste la gramática como argumento
        grammar = sys.argv[1]
        run_with_grammar(grammar)
    else:
        # Modo 2: Interactivo - te pregunta
        modo_interactivo()
