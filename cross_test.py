"""
FRAMEWORK DE VALIDACIÓN SINTÁCTICA - CURSO 2025-2026
Desarrollado por: Carla Lombaar
"""

import os
import sys
import re
from datetime import datetime

# Carga de librerías profesionales
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(">>> ALERTA: Ejecuta 'pip install requests beautifulsoup4' para continuar.")
    sys.exit(1)

class AnalizadorPro:
    def __init__(self):
        # Configuración visual y etiquetas a analizar
        self.CLR = {'tit': "\033[94m", 'ok': "\033[92m", 'err': "\033[91m", 'res': "\033[0m", 'bold': "\033[1m"}
        self.tags_analizar = ['a', 'img', 'div', 'p', 'span', 'ul', 'li', 'table', 'tr', 'td', 'br']

    def mostrar_logo(self):
        """Genera un banner visual en la terminal."""
        print(f"{self.CLR['tit']}{self.CLR['bold']}" + "•"*60)
        print("     SISTEMA DE VERIFICACIÓN DE DOM - BY CARLA LOMBAAR     ")
        print("•"*60 + f"{self.CLR['res']}")

    def capturar_contenido(self, origen):
        """Extrae el HTML de fuentes remotas o archivos locales."""
        if "https://" in origen.lower():
            req = requests.get(origen)
            req.raise_for_status()
            return req.text
        else:
            if not os.path.isfile(origen):
                raise FileNotFoundError(f"Archivo '{origen}' no localizado.")
            with open(origen, 'r', encoding='utf-8') as f:
                return f.read()

    def extraer_info(self, html):
        """Analiza el árbol de etiquetas usando BeautifulSoup."""
        dom = BeautifulSoup(html, 'html.parser')
        
        # Extracción estricta de recursos
        coleccion_links = [tag['href'] for tag in dom.find_all('a', href=True)]
        coleccion_imgs = [tag['src'] for tag in dom.find_all('img', src=True)]
        
        # Conteo de frecuencia de etiquetas
        conteo_nodos = {t: len(dom.find_all(t)) for t in self.tags_analizar}
        
        return coleccion_links, coleccion_imgs, conteo_nodos

    def generar_log(self, data, tipo, base_name):
        """Guarda los resultados en ficheros con marca de tiempo única."""
        marca = datetime.now().strftime("%Y_%H%M%S")
        slug = re.sub(r'\W+', '', base_name)[:10]
        archivo_nombre = f"LOG_{tipo}_{slug}_{marca}.txt"
        
        with open(archivo_nombre, 'w', encoding='utf-8') as f:
            f.write("\n".join(data))
        return archivo_nombre

    def ejecutar(self):
        """Controlador del flujo de la aplicación."""
        self.mostrar_logo()
        
        while True:
            target = input(f"\n{self.CLR['bold']}🔍 Inserte HTML o URL a auditar (o Enter para salir): {self.CLR['res']}").strip()
            if not target: break

            try:
                raw_html = self.capturar_contenido(target)
                links, imagenes, stats = self.extraer_info(raw_html)

                print(f"\n{self.CLR['tit']}--- RESULTADOS DE LA AUDITORÍA ---{self.CLR['res']}")
                print(f"[{self.CLR['ok']}OK{self.CLR['res']}] Recurso: {target}")
                print(f"[{self.CLR['ok']}OK{self.CLR['res']}] Enlaces: {len(links)} | Imágenes: {len(imagenes)}")
                
                print(f"\n{self.CLR['bold']}Densidad de etiquetas (Estadísticas):{self.CLR['res']}")
                for tag, total in stats.items():
                    print(f"  <{tag}>: {total}")

                # Persistencia de los resultados
                f1 = self.generar_log(links, "ENLACES", target)
                f2 = self.generar_log(imagenes, "IMAGENES", target)
                print(f"\n{self.CLR['ok']} Auditoría exportada a: {f1} y {f2}{self.CLR['res']}")

            except Exception as e:
                print(f"{self.CLR['err']} ERROR EN EL PROCESO: {e}{self.CLR['res']}")

if __name__ == "__main__":
    app = AnalizadorPro()
    app.ejecutar()