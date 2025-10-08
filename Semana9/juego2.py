import ollama
import os
import time
from datetime import datetime

# ============ CONFIGURACIÓN ============
MODELO = "gemma3:4b"  # Cambia por "tinyllama" si tienes poca RAM
CARPETA_VERSIONES = "versiones_juego"
TIEMPO_ESPERA = 120  # segundos entre iteraciones (2 minutos)

# Crear carpeta para versiones
if not os.path.exists(CARPETA_VERSIONES):
    os.makedirs(CARPETA_VERSIONES)

# ============ JUEGO BASE ============
codigo_juego = """import pygame
import random

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Evolutivo")
reloj = pygame.time.Clock()

# Jugador
jugador = pygame.Rect(ANCHO//2, ALTO//2, 30, 30)
velocidad = 5

# Juego principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    # Controles
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.x > 0:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - jugador.width:
        jugador.x += velocidad
    if teclas[pygame.K_UP] and jugador.y > 0:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN] and jugador.y < ALTO - jugador.height:
        jugador.y += velocidad
    
    # Dibujar
    pantalla.fill((0, 0, 0))
    pygame.draw.rect(pantalla, (0, 255, 0), jugador)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
"""

# ============ FUNCIÓN DE MEJORA ============
def mejorar_juego(codigo_actual, comentario_usuario="", iteracion_num=0):
    """Envía el código a Ollama para que lo mejore"""
    
    mejoras_sugeridas = [
        "añade enemigos que se muevan",
        "agrega sistema de puntuación",
        "implementa colisiones",
        "añade power-ups o items",
        "mejora los gráficos y colores",
        "agrega efectos de sonido o música",
        "implementa niveles de dificultad",
        "añade pantalla de game over"
    ]
    
    # Si no hay comentario del usuario, sugiere una mejora automática
    if not comentario_usuario:
        comentario_usuario = mejoras_sugeridas[iteracion_num % len(mejoras_sugeridas)]
    
    prompt = f"""Eres un desarrollador experto en Python y Pygame. Mejora este juego de forma incremental.

MEJORA A IMPLEMENTAR: {comentario_usuario}

REGLAS IMPORTANTES:
1. Haz UNA mejora clara y funcional
2. El código debe ejecutarse sin errores
3. Mantén la estructura básica de Pygame
4. NO uses archivos externos (imágenes, sonidos)
5. Comenta brevemente los cambios nuevos
6. Asegúrate que el juego sea jugable

CÓDIGO ACTUAL:
{codigo_actual}

RESPONDE SOLO CON EL CÓDIGO COMPLETO MEJORADO, sin explicaciones antes o después del código.
"""
    
    try:
        print("   🤖 Pensando en mejoras...")
        respuesta = ollama.chat(model=MODELO, messages=[{
            'role': 'user',
            'content': prompt
        }])
        
        contenido = respuesta['message']['content']
        
        # Extraer solo el código Python
        if '```python' in contenido:
            inicio = contenido.find('```python') + 9
            fin = contenido.find('```', inicio)
            codigo = contenido[inicio:fin].strip()
        elif '```' in contenido:
            inicio = contenido.find('```') + 3
            fin = contenido.find('```', inicio)
            codigo = contenido[inicio:fin].strip()
        else:
            codigo = contenido.strip()
        
        return codigo
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

# ============ GUARDAR VERSIÓN ============
def guardar_version(codigo, iteracion, comentario=""):
    """Guarda una versión del juego"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"juego_v{iteracion}_{timestamp}.py"
    ruta_completa = os.path.join(CARPETA_VERSIONES, nombre_archivo)
    
    # Agregar comentario en el código
    header = f"""# Versión {iteracion}
# Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Mejora: {comentario if comentario else "Mejora automática"}
# ============================================

"""
    
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        f.write(header + codigo)
    
    return ruta_completa

# ============ EJECUTAR JUEGO ============
def ejecutar_juego(ruta_archivo):
    """Ejecuta el juego en una nueva ventana"""
    import subprocess
    import sys
    
    print(f"\n🎮 Ejecutando juego: {ruta_archivo}")
    print("   Cierra la ventana del juego para continuar...")
    
    try:
        # Ejecuta el juego en un proceso separado
        subprocess.run([sys.executable, ruta_archivo])
        print("✅ Juego cerrado")
    except Exception as e:
        print(f"❌ Error ejecutando el juego: {e}")

# ============ LOOP PRINCIPAL ============
def main():
    global codigo_juego
    
    print("=" * 60)
    print("🎮 SISTEMA DE EVOLUCIÓN DE JUEGOS CON IA")
    print("=" * 60)
    print(f"📦 Modelo: {MODELO}")
    print(f"📁 Versiones en: ./{CARPETA_VERSIONES}/")
    print("=" * 60)
    
    # Guardar versión inicial
    ruta = guardar_version(codigo_juego, 0, "Versión inicial")
    print(f"\n✅ Versión inicial guardada: {ruta}")
    
    iteracion = 1
    
    try:
        while True:
            print(f"\n{'='*60}")
            print(f"🔄 ITERACIÓN {iteracion}")
            print('='*60)
            
            # Preguntar al usuario
            print("\n💬 ¿Qué mejora quieres? (Enter para automático)")
            print("   Ejemplos: 'enemigos', 'puntos', 'más rápido', 'colores'")
            print("   Escribe 'salir' para terminar")
            
            comentario = input("\n👉 Tu comentario: ").strip()
            
            if comentario.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break
            
            # Mejorar el juego
            print(f"\n🔧 Aplicando mejora...")
            nuevo_codigo = mejorar_juego(codigo_juego, comentario, iteracion)
            
            if nuevo_codigo and len(nuevo_codigo) > 100:
                # Guardar nueva versión
                ruta = guardar_version(nuevo_codigo, iteracion, comentario if comentario else "automático")
                print(f"✅ Nueva versión guardada: {ruta}")
                print(f"📊 Tamaño del código: {len(nuevo_codigo)} caracteres")
                
                codigo_juego = nuevo_codigo
                iteracion += 1
                
                print(f"\n⏰ Esperando {TIEMPO_ESPERA} segundos...")
                print("   (Presiona Ctrl+C para dar siguiente comentario)")
                
                try:
                    time.sleep(TIEMPO_ESPERA)
                except KeyboardInterrupt:
                    print("\n⏭️  Saltando espera...")
                    continue
            else:
                print("❌ No se pudo generar una mejora válida")
                print("   Reintentando en la siguiente iteración...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Sistema detenido por el usuario")
    
    print(f"\n📊 Total de versiones generadas: {iteracion}")
    print(f"📁 Revisa las versiones en: ./{CARPETA_VERSIONES}/")

# ============ EJECUTAR ============
if __name__ == "__main__":
    main()