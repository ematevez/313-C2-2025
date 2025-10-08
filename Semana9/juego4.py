import ollama
import os
import subprocess
import sys
import time
import random
import threading
from datetime import datetime

# ============ CONFIGURACIÓN ============
MODELO = "qwen3:8b"
ARCHIVO_JUEGO = "juego_evolutivo.py"
ARCHIVO_HISTORIAL = "historial_mejoras.txt"
TIEMPO_AUTO = 300  # segundos sin input antes de mejora automática

input_recibido = None
timeout_ocurrido = False

# ============ JUEGO BASE ============
codigo_juego = """import pygame
import random

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Evolutivo")
reloj = pygame.time.Clock()

jugador = pygame.Rect(ANCHO//2, ALTO//2, 30, 30)
velocidad = 5

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.x > 0:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - jugador.width:
        jugador.x += velocidad
    if teclas[pygame.K_UP] and jugador.y > 0:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN] and jugador.y < ALTO - jugador.height:
        jugador.y += velocidad
    
    pantalla.fill((0, 0, 0))
    pygame.draw.rect(pantalla, (0, 255, 0), jugador)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
"""

# ============ MEJORAS POSIBLES ============
MEJORAS_ALEATORIAS = [
    "añade 3 enemigos rojos que se muevan aleatoriamente",
    "agrega sistema de puntuación en la esquina superior izquierda",
    "implementa game over cuando el jugador toca un enemigo",
    "añade 2 power-ups azules que aparezcan aleatoriamente y den puntos",
    "mejora los gráficos con colores más vibrantes",
    "implementa que los enemigos se muevan más rápido cada 10 segundos",
    "añade un enemigo verde que persiga al jugador lentamente",
    "agrega un contador de tiempo jugado en pantalla",
    "implementa sistema de 3 vidas para el jugador",
    "añade un fondo azul oscuro con estrellas blancas pequeñas",
    "crea enemigos amarillos que se muevan en diagonal",
    "agrega pantalla de game over con el puntaje final",
    "implementa que al recoger power-ups el jugador sea más rápido temporalmente",
    "añade más enemigos cuando sube el puntaje",
    "implementa bordes de colores en la pantalla"
]

# ============ INPUT CON TIMEOUT ============
def input_con_timeout(prompt, timeout):
    global input_recibido, timeout_ocurrido
    input_recibido = None
    timeout_ocurrido = False

    def obtener_input():
        global input_recibido
        try:
            input_recibido = input(prompt)
        except:
            pass

    thread = threading.Thread(target=obtener_input)
    thread.daemon = True
    thread.start()

    tiempo_inicial = time.time()
    while (time.time() - tiempo_inicial) < timeout:
        if input_recibido is not None:
            return input_recibido
        tiempo_restante = int(timeout - (time.time() - tiempo_inicial))
        print(f"\r⏰ Mejora automática en: {tiempo_restante}s (escribe algo o espera)...", end='', flush=True)
        time.sleep(1)

    print("\r⏰ ¡Tiempo cumplido! Mejora automática activada...           ")
    timeout_ocurrido = True
    return None

# ============ VERIFICAR SINTAXIS ============
def verificar_sintaxis(codigo):
    try:
        compile(codigo, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

# ============ CORREGIR ERRORES ============
def corregir_codigo(codigo_con_error, mensaje_error):
    prompt = f"""Corrige el siguiente código de Python con error de sintaxis.

ERROR DETECTADO:
{mensaje_error}

CÓDIGO CON ERROR:
{codigo_con_error}

REGLAS:
1. Corrige SOLO el error de sintaxis.
2. No agregues nuevas funciones ni modifiques la lógica del juego.
3. Devuelve solo el código corregido, sin texto adicional."""
    try:
        print("   🔧 IA corrigiendo errores...")
        respuesta = ollama.chat(model=MODELO, messages=[{'role': 'user', 'content': prompt}])
        contenido = respuesta['message']['content']
        if '```' in contenido:
            codigo = contenido.split('```')[1].replace('python', '').strip()
        else:
            codigo = contenido.strip()
        return codigo
    except Exception as e:
        print(f"   ❌ Error al corregir: {e}")
        return None

# ============ PRUEBA RÁPIDA ============
def prueba_rapida(codigo):
    try:
        exec(codigo, {"__name__": "__main__"})
        return True
    except Exception as e:
        print(f"   ⚠️  Error en ejecución de prueba: {e}")
        return False

# ============ MEJORAR JUEGO ============
def mejorar_juego(codigo_actual, comentario_usuario=""):
    if not comentario_usuario:
        comentario_usuario = random.choice(MEJORAS_ALEATORIAS)
        print(f"   🎲 Mejora aleatoria elegida: {comentario_usuario}")

    prompt = f"""Eres un desarrollador experto en Python y Pygame. Mejora el siguiente juego.

MEJORA A IMPLEMENTAR: {comentario_usuario}

REGLAS:
1. Implementa exactamente la mejora solicitada.
2. Mantén la estructura principal de Pygame (init, loop, quit).
3. No uses archivos externos ni dependencias nuevas.
4. Asegúrate de que el código sea completamente válido y funcional.

CÓDIGO ACTUAL:
{codigo_actual}

RESPONDE SOLO CON EL CÓDIGO COMPLETO MEJORADO."""
    try:
        print("   🤖 IA generando mejora...")
        respuesta = ollama.chat(model=MODELO, messages=[{'role': 'user', 'content': prompt}])
        contenido = respuesta['message']['content']
        if '```' in contenido:
            codigo = contenido.split('```')[1].replace('python', '').strip()
        else:
            codigo = contenido.strip()
        return codigo
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

# ============ GUARDAR Y EJECUTAR ============
def guardar_y_ejecutar(codigo, iteracion, comentario=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# Iteración {iteracion} - {timestamp}\n# Mejora: {comentario or 'Automática'}\n# ============================================\n\n"

    with open(ARCHIVO_JUEGO, 'w', encoding='utf-8') as f:
        f.write(header + codigo)
    with open(ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\nIteración {iteracion} - {timestamp}\nMejora: {comentario or 'Automática'}\n{'='*60}\n")

    print(f"   ✅ Código guardado en: {ARCHIVO_JUEGO}")
    print(f"\n   🎮 Ejecutando juego (cierra la ventana para continuar)...")
    try:
        subprocess.run([sys.executable, ARCHIVO_JUEGO])
        print("\n   ✅ Juego cerrado - Continuando evolución...\n")
    except Exception:
        print("   ⚠️  Juego cerrado manualmente o con error no crítico.")

# ============ LOOP PRINCIPAL ============
def main():
    global codigo_juego
    print("=" * 70)
    print("🎮 SISTEMA DE EVOLUCIÓN AUTOMÁTICA DE JUEGOS (versión robusta)")
    print("=" * 70)
    print(f"📦 Modelo IA: {MODELO}")
    print(f"📄 Archivo: {ARCHIVO_JUEGO}")
    print(f"⏰ Auto-mejora cada: {TIEMPO_AUTO//60} minutos sin input")
    print("=" * 70)

    if os.path.exists(ARCHIVO_HISTORIAL):
        os.remove(ARCHIVO_HISTORIAL)

    print("\n🎯 Guardando versión inicial...")
    guardar_y_ejecutar(codigo_juego, 0, "Versión inicial básica")

    iteracion = 1

    try:
        while True:
            print(f"\n{'='*70}")
            print(f"🔄 ITERACIÓN {iteracion}")
            print('='*70)
            print("\n💬 ¿Qué mejora quieres?")
            print("   Ejemplos: 'enemigos rojos', 'sistema de puntos', 'más difícil'")
            print("   'salir' = Terminar programa\n")

            comentario = input_con_timeout("👉 Tu comentario: ", TIEMPO_AUTO)

            if comentario and comentario.strip().lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break

            comentario = comentario.strip() if comentario else ""
            print("\n🔧 Generando mejora...")
            nuevo_codigo = mejorar_juego(codigo_juego, comentario)

            if nuevo_codigo and len(nuevo_codigo) > 100:
                print("   🔍 Verificando sintaxis...")
                es_valido, error = verificar_sintaxis(nuevo_codigo)
                intentos = 0
                while not es_valido and intentos < 2:
                    intentos += 1
                    print(f"   ⚠️  Error de sintaxis ({intentos}/2): {error}")
                    nuevo_codigo = corregir_codigo(nuevo_codigo, error)
                    if not nuevo_codigo:
                        break
                    es_valido, error = verificar_sintaxis(nuevo_codigo)

                if es_valido and prueba_rapida(nuevo_codigo):
                    print("   ✅ Código válido y ejecutable.")
                    guardar_y_ejecutar(nuevo_codigo, iteracion, comentario or "Mejora automática aleatoria")
                    codigo_juego = nuevo_codigo
                    iteracion += 1
                else:
                    print("   ❌ Fallo tras correcciones. Guardando versión rota y regenerando...")
                    with open(f"juego_fallido_iter{iteracion}.py", "w", encoding="utf-8") as f:
                        f.write(nuevo_codigo or "# Código vacío\n")

                    intento_regeneracion = mejorar_juego(codigo_juego, f"Reconstruir correctamente la mejora: {comentario}")
                    if intento_regeneracion:
                        es_valido, error = verificar_sintaxis(intento_regeneracion)
                        if es_valido and prueba_rapida(intento_regeneracion):
                            print("   ✅ Regeneración exitosa.")
                            guardar_y_ejecutar(intento_regeneracion, iteracion, comentario + " (reconstrucción)")
                            codigo_juego = intento_regeneracion
                            iteracion += 1
                        else:
                            print("   ⚠️  Regeneración fallida. Manteniendo versión anterior.")
                    else:
                        print("   ⚠️  No se pudo regenerar. Continuando con versión estable.")
            else:
                print("   ❌ Respuesta de IA inválida o demasiado corta. Reintentando...")

    except KeyboardInterrupt:
        print("\n👋 Sistema detenido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

    print(f"\n📊 Total de iteraciones: {iteracion}")
    print(f"🎮 Juego final guardado en: {ARCHIVO_JUEGO}")

if __name__ == "__main__":
    main()
