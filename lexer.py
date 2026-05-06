"""
PROYECTO DE SCRAPING - CURSO 2025-2026
Componente: Analizador Léxico (Lexer)

Este módulo se encarga de la tokenización del código HTML para:
1. Identificar la estructura de etiquetas (apertura/cierre) y verificar el balanceo.
2. Extraer enlaces mediante el atributo 'href'.
3. Localizar rutas de imágenes mediante el atributo 'src'.
"""

import ply.lex as lex
import re

# Listado de componentes léxicos identificables
tokens = (
    'ETIQUETA_APERTURA',
    'ETIQUETA_CIERRE',
    'ATRIBUTO_HREF',
    'ATRIBUTO_SRC',
)

# --- REGLAS DE EXCLUSIÓN ---
# Se omiten comentarios y la declaración del DOCTYPE para evitar ruido en el análisis
t_ignore_COMENTARIOS = r'<!--(.|\n)*?-->'
t_ignore_DOCTYPE = r'<!DOCTYPE[^>]*>'

# --- DEFINICIÓN DE TOKENS MEDIANTE FUNCIONES ---

# Captura de etiquetas de cierre: </nombre_tag>
def t_ETIQUETA_CIERRE(t):
    r'<\s*/\s*[a-zA-Z][a-zA-Z0-9]*\s*>'
    # Normalización: eliminamos símbolos y pasamos a minúsculas
    t.value = re.sub(r'[</>\s]', '', t.value).lower()
    return t

# Captura de etiquetas de apertura: <nombre_tag
def t_ETIQUETA_APERTURA(t):
    r'<\s*[a-zA-Z][a-zA-Z0-9]*'
    # Limpieza de caracteres de control
    t.value = t.value.replace('<', '').strip().lower()
    return t

# Extracción de URL en hipervínculos
def t_ATRIBUTO_HREF(t):
    r'href\s*=\s*\"[^\"]*\"'
    # Procesamiento del string para obtener solo el contenido de las comillas
    partes = t.value.split('"')
    t.value = partes[1] if len(partes) > 1 else t.value
    return t

# Extracción de fuentes de imagen
def t_ATRIBUTO_SRC(t):
    r'src\s*=\s*\"[^\"]*\"'
    # Usamos búsqueda de comillas para limpiar el valor
    t.value = re.findall(r'\"(.*?)\"', t.value)[0]
    return t

# Caracteres a ignorar por defecto
t_ignore = ' \t\r\n'

# Gestión de caracteres no reconocidos
def t_error(t):
    # Descartamos el carácter y continuamos la ejecución
    t.lexer.skip(1)

# Constructor del motor léxico
def generar_lexer(**kwargs):
    # Configuramos flags para ignorar mayúsculas y permitir multilínea en regex
    return lex.lex(reflags=re.IGNORECASE | re.DOTALL, **kwargs)

# --- MÓDULO DE PRUEBAS ---
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Error: Se requiere un archivo HTML de entrada.')
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        analizador = generar_lexer()
        analizador.input(contenido)
        
        print(f"Iniciando análisis de tokens para: {sys.argv[1]}")
        for token in analizador:
            print(f"Tipo: {token.type:20} | Valor: {token.value}")
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {sys.argv[1]}")