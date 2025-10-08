import ollama
import os
import subprocess
import sys
import time
from datetime import datetime

# ============ CONFIGURACIÓN ============
MODELO =  "gemma3:4b"  # Cambia por "gemma3:4b" o "tinyllama" según tu modelo
ARCHIVO_JUEGO = "juego_evolutivo.py"
ARCHIVO_HISTORIAL = "historial_mejoras.txt"
TIEMPO_ESPERA = 60  # segundos entre iteraciones (1 minuto)

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
        "añade enemigos rojos que se muevan aleatoriamente",
        "agrega sistema de puntuación en la esquina",
        "implementa colisiones entre jugador y enemigos con game over",
        "añade power-ups azules que dan puntos extra",
        "mejora los gráficos con colores vibrantes y efectos",
        "implementa niveles de dificultad creciente",
        "añade más tipos de enemigos con diferentes comportamientos",
        "agrega efectos visuales cuando hay colisiones"
    ]
    
    # Si no hay comentario del usuario, sugiere una mejora automática
    if not comentario_usuario:
        comentario_usuario = mejoras_sugeridas[iteracion_num % len(mejoras_sugeridas)]
    
    prompt = f"""Eres un desarrollador experto en Python y Pygame. Mejora este juego de forma incremental.

MEJORA A IMPLEMENTAR: {comentario_usuario}

REGLAS IMPORTANTES:
1. Haz UNA mejora clara y funcional basada en la solicitud
2. El código debe ejecutarse sin errores
3. Mantén la estructura básica de Pygame
4. NO uses archivos externos (imágenes, sonidos)
5. Agrega un comentario breve al inicio explicando la mejora
6. Asegúrate que el juego sea completamente jugable
7. Mantén el control con las flechas del teclado

CÓDIGO ACTUAL:
{codigo_actual}

RESPONDE SOLO CON EL CÓDIGO COMPLETO MEJORADO, sin explicaciones antes o después del código.
"""
    
    try:
        print("   🤖 IA pensando en mejoras...")
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

# ============ GUARDAR Y EJECUTAR ============
def guardar_y_ejecutar(codigo, iteracion, comentario=""):
    """Guarda el código y lo ejecuta inmediatamente"""
    
    # Agregar header con info de la mejora
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"""# Iteración {iteracion} - {timestamp}
# Mejora: {comentario if comentario else "Mejora automática"}
# ============================================

"""
    
    # Guardar código
    with open(ARCHIVO_JUEGO, 'w', encoding='utf-8') as f:
        f.write(header + codigo)
    
    # Guardar en historial
    with open(ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Iteración {iteracion} - {timestamp}\n")
        f.write(f"Mejora: {comentario if comentario else 'Automática'}\n")
        f.write(f"{'='*60}\n")
    
    print(f"✅ Código guardado en: {ARCHIVO_JUEGO}")
    
    # Ejecutar el juego
    print(f"\n🎮 EJECUTANDO JUEGO (Cierra la ventana para continuar)...")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, ARCHIVO_JUEGO])
        print("\n✅ Juego cerrado - Continuando evolución...\n")
    except Exception as e:
        print(f"❌ Error ejecutando el juego: {e}")

# ============ LOOP PRINCIPAL ============
def main():
    global codigo_juego
    
    print("=" * 60)
    print("🎮 SISTEMA DE EVOLUCIÓN AUTOMÁTICA DE JUEGOS")
    print("=" * 60)
    print(f"📦 Modelo IA: {MODELO}")
    print(f"📄 Archivo único: {ARCHIVO_JUEGO}")
    print(f"📋 Historial: {ARCHIVO_HISTORIAL}")
    print("=" * 60)
    
    # Limpiar historial anterior
    if os.path.exists(ARCHIVO_HISTORIAL):
        os.remove(ARCHIVO_HISTORIAL)
    
    # Guardar y ejecutar versión inicial
    print("\n🎯 Guardando versión inicial...")
    guardar_y_ejecutar(codigo_juego, 0, "Versión inicial básica")
    
    iteracion = 1
    
    try:
        while True:
            print(f"\n{'='*60}")
            print(f"🔄 ITERACIÓN {iteracion}")
            print('='*60)
            
            # Preguntar al usuario
            print("\n💬 ¿Qué mejora quieres?")
            print("   Ejemplos: 'enemigos', 'puntos', 'más rápido', 'colores'")
            print("   Enter = Mejora automática")
            print("   'salir' = Terminar programa")
            
            comentario = input("\n👉 Tu comentario: ").strip()
            
            if comentario.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego! El juego final está en:", ARCHIVO_JUEGO)
                break
            
            # Mejorar el juego
            print(f"\n🔧 Aplicando mejora...")
            nuevo_codigo = mejorar_juego(codigo_juego, comentario, iteracion)
            
            if nuevo_codigo and len(nuevo_codigo) > 100:
                # Guardar y ejecutar inmediatamente
                guardar_y_ejecutar(nuevo_codigo, iteracion, comentario if comentario else "automático")
                
                codigo_juego = nuevo_codigo
                iteracion += 1
                
                # Espera antes de siguiente iteración
                print(f"⏰ Próxima mejora en {TIEMPO_ESPERA} segundos...")
                print("   (Presiona Ctrl+C para dar siguiente comentario ahora)")
                
                try:
                    time.sleep(TIEMPO_ESPERA)
                except KeyboardInterrupt:
                    print("\n⏭️  Saltando espera...")
                    continue
            else:
                print("❌ No se pudo generar una mejora válida, reintentando...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Sistema detenido por el usuario")
    
    print(f"\n📊 Total de iteraciones: {iteracion}")
    print(f"🎮 Juego final guardado en: {ARCHIVO_JUEGO}")
    print(f"📋 Historial de mejoras en: {ARCHIVO_HISTORIAL}")

# ============ EJECUTAR ============
if __name__ == "__main__":
    main()