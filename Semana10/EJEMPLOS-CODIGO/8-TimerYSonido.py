import pygame
from constantes import *
segundos = "12"
fin_tiempo = False
#iniciar la pantalla
pygame.init()

#Defino un Timer
timer_segundos = pygame.USEREVENT
timer_2_segundos = pygame.USEREVENT+1
pygame.time.set_timer(timer_segundos,1000) #1000 es 1 segundo
pygame.time.set_timer(timer_2_segundos,2000) #2000 son 2 segundos

#Defino musica
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("y2mate.mp3")
volumen = 0.09
sonido_fondo.set_volume(volumen)

#Defino la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

#Defino el titulo
pygame.display.set_caption("PyGame")

#Defino texto
fuente = pygame.font.SysFont("Arial", 80)

flag_correr = True
while flag_correr:
    sonido_fondo.play()
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.USEREVENT:
            if evento.type == timer_segundos:
                if fin_tiempo == False:
                    segundos = int(segundos) - 1
                    volumen = volumen - 0.01
                    sonido_fondo.set_volume(volumen)
                    if int(segundos) == 0:
                        fin_tiempo = True
                        segundos = "Tiempo"
                        sonido_fondo.stop()
        if evento.type == pygame.USEREVENT+1:
            if evento.type == timer_2_segundos:
                print("pasaron 2 segundos")
    
    pantalla.fill(COLOR_ROJO)
    segundos_texto = fuente.render(str(segundos), True, COLOR_BLANCO )
    pantalla.blit(segundos_texto, POS_TIMER)
    pygame.display.flip()
sonido_fondo.stop()
pygame.quit()