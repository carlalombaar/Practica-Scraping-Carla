from parser import ejecutar_analisis
import sys

def generar_reporte(archivo_entrada):
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        links, imagenes, balanceado = ejecutar_analisis(contenido)
        
        nombre_salida = "resultado_" + archivo_entrada.replace(".html", ".txt")
        
        with open(nombre_salida, 'w', encoding='utf-8') as f_out:
            f_out.write(f"REPORTE DE SCRAPING: {archivo_entrada}\n")
            # Usamos una variable intermedia para evitar el error de comillas
            estado_texto = "SI" if balanceado else "NO"
            f_out.write(f"Estructura balanceada: {estado_texto}\n")
            f_out.write("-" * 30 + "\n")
            f_out.write(f"ENLACES ENCONTRADOS ({len(links)}):\n")
            for l in links: f_out.write(f"- {l}\n")
            f_out.write(f"\nIMÁGENES ENCONTRADAS ({len(imagenes)}):\n")
            for i in imagenes: f_out.write(f"- {i}\n")
            
        print(f"✅ EXITO: Generado {nombre_salida}")

    except Exception as e:
        print(f"❌ ERROR en {archivo_entrada}: {e}")

if __name__ == "__main__":
    # Aseguramos que 'archivo' se defina SIEMPRE antes de usarse
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = "prueba1.html"
    
    generar_reporte(archivo)