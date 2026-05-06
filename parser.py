"""
PROYECTO DE SCRAPING - CURSO 2025-2026
Componente: Analizador Sintáctico (Parser) y Validador de Estructura

Este módulo procesa los tokens generados por el lexer para:
1. Validar el balanceo de etiquetas mediante una pila (stack).
2. Extraer enlaces e imágenes basándose en el contexto de la etiqueta.
"""

import ply.yacc as yacc
# Importamos la lista de tokens y el constructor desde tu lexer.py
from lexer import tokens, generar_lexer 

# --- VARIABLES DE ALMACENAMIENTO ---
lista_links = []      # Almacena URLs de href en <a>
lista_recursos = []   # Almacena URLs de src en <img>
pila_etiquetas = []   # Pila para verificar el balanceo
estado_balanceo = True # Indica si el HTML es estructuralmente correcto

# Elementos que no tienen etiqueta de cierre según el estándar HTML
VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img',
    'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'
}

# --- REGLAS DE LA GRAMÁTICA (PLY) ---

def p_documento(p):
    'documento : bloque_elementos'
    pass

def p_bloque_elementos(p):
    '''bloque_elementos : elemento bloque_elementos
                        | vacio'''
    pass

def p_elemento(p):
    '''elemento : ETIQUETA_APERTURA
                | ETIQUETA_CIERRE
                | ATRIBUTO_HREF
                | ATRIBUTO_SRC'''
    pass

def p_vacio(p):
    'vacio :'
    pass

def p_error(p):
    # Los errores sintácticos se gestionan mediante la lógica de la pila
    pass

# --- FUNCIÓN PRINCIPAL DE ANÁLISIS ---

def ejecutar_analisis(texto_html):
    global lista_links, lista_recursos, pila_etiquetas, estado_balanceo
    
    # Reiniciamos las variables globales para cada nueva ejecución
    lista_links = []
    lista_recursos = []
    pila_etiquetas = []
    estado_balanceo = True
    tag_actual = None 

    # Inicializamos el lexer y el motor del parser
    analizador_lexico = generar_lexer()
    motor_sintactico = yacc.yacc()
    analizador_lexico.input(texto_html)

    # Recorremos los tokens uno a uno
    for unidad in analizador_lexico:
        tipo = unidad.type
        # Normalizamos el nombre de la etiqueta a minúsculas
        valor = unidad.value.lower() if tipo in ('ETIQUETA_APERTURA', 'ETIQUETA_CIERRE') else unidad.value

        if tipo == 'ETIQUETA_APERTURA':
            tag_actual = valor
            if valor == 'a':
                pila_etiquetas.append('a')
            elif valor == 'img':
                pass  # Las imágenes no se apilan por ser auto-cerrantes
            elif valor in VOID_ELEMENTS:
                tag_actual = None # No esperamos atributos dentro de otros void elements
            else:
                pila_etiquetas.append(valor)
            continue

        if tipo == 'ETIQUETA_CIERRE':
            tag_actual = None
            if valor in VOID_ELEMENTS:
                continue
            
            # Verificación del balanceo mediante la pila
            if not pila_etiquetas or pila_etiquetas[-1] != valor:
                estado_balanceo = False
            else:
                pila_etiquetas.pop()
            continue

        if tipo == 'ATRIBUTO_HREF':
            # Solo extraemos el link si el contexto actual es una etiqueta <a>
            if tag_actual == 'a':
                lista_links.append(unidad.value)
            continue

        if tipo == 'ATRIBUTO_SRC':
            # Solo extraemos la ruta si el contexto actual es una etiqueta <img>
            if tag_actual == 'img':
                lista_recursos.append(unidad.value)
            tag_actual = None # Tras encontrar el src, cerramos el contexto de img
            continue

    # Si al final la pila no está vacía, el HTML está desbalanceado
    if pila_etiquetas:
        estado_balanceo = False

    return lista_links, lista_recursos, estado_balanceo

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python parser.py <tu_archivo.html>")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html_input = f.read()
        
        links, imagenes, balanceado = ejecutar_analisis(html_input)
        
        print(f"\n--- RESULTADOS DEL ANÁLISIS ---")
        print(f"Archivo analizado: {sys.argv[1]}")
        print(f"Total Enlaces (<a>): {len(links)}")
        print(f"Total Imágenes (<img>): {len(imagenes)}")
        print(f"¿Estructura Balanceada?: {'SÍ' if balanceado else 'NO'}")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{sys.argv[1]}'")