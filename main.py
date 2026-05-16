import os
import re
import sys
import requests
# Importamos TU función del parser
from parser import ejecutar_analisis 

# --- CONFIGURACIÓN DE ESTILOS (ANSI) ---
CSI = "\033["
END = CSI + "0m"
BOLD = CSI + "1m"
RED = CSI + "31m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
CYAN = CSI + "36m"

def banner():
    print(BOLD + CYAN + "="*60 + END)
    print(BOLD + CYAN + "     🕸️  SISTEMA DE SCRAPING PRO - CARLA LOMBAAR  🕸️     " + END)
    print(BOLD + CYAN + "="*60 + END)
    print(f"{YELLOW}Archivos soportados:{END} local [.html], URLs [https://]")
    print()

def cargar_contenido(origen: str) -> str:
    if origen.lower().startswith('https://') or origen.lower().startswith('http://'):
        # Descarga el HTML desde internet
        resp = requests.get(origen, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        resp.raise_for_status()
        return resp.text
    else:
        # Carga el archivo local
        if not os.path.isfile(origen):
            raise FileNotFoundError(f"No se encuentra el archivo '{origen}'.")
        with open(origen, 'r', encoding='utf-8') as f:
            return f.read()

def guardar_lista(lista, nombre_fichero):
    with open(nombre_fichero, 'w', encoding='utf-8') as f:
        for item in lista:
            f.write(item + '\n')

def main():
    banner()
    while True:
        origen = input(BOLD + "  Origen (.html/ o URL): " + END).strip()
        if not origen:
            print(GREEN + "  ¡Hasta pronto!" + END)
            break

        try:
            # 1. Obtenemos el HTML
            html = cargar_contenido(origen)
            
            # 2. Tu parser (ejecutar_analisis devuelve links, imagenes, balance)
            enlaces, imagenes, balance_ok = ejecutar_analisis(html)

            # 3. Mostrar resultados por pantalla (Estilo Jaime)
            print("\n" + BOLD + CYAN + "-"*50 + END)
            print(BOLD + "Origen: " + END + origen)
            print(BOLD + "- Enlaces (href):" + END, f"{len(enlaces)}")
            for u in enlaces:
                print("   •", u)
            
            print(BOLD + "- Imágenes (src):" + END, f"{len(imagenes)}")
            for u in imagenes:
                print("   •", u)

            # Resultado del balanceo
            bal_text = (GREEN + "SÍ" + END) if balance_ok else (RED + "NO" + END)
            print(BOLD + "- HTML balanceado:" + END, bal_text)
            print(BOLD + CYAN + "-"*50 + END + "\n")

            # 4. Guardar resultados (Sanitización para evitar el Error 22)
            safe_name = re.sub(r'[^0-9A-Za-z]+', '_', origen).strip('_')
            f_links = f"enlaces_{safe_name}.txt"
            f_imgs  = f"imagenes_{safe_name}.txt"
            
            guardar_lista(enlaces, f_links)
            guardar_lista(imagenes, f_imgs)
            
            print(GREEN + f"  ÉXITO: Guardado '{f_links}'" + END)
            print(GREEN + f"  ÉXITO: Guardado '{f_imgs}'\n" + END)

        except Exception as e:
            print(RED + " ERROR:" + END, e)
            print()

if __name__ == '__main__':
    main()