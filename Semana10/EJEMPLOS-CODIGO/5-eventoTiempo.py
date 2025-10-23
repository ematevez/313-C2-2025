import pygame
#iniciar la pantalla
pygame.init()
#COLORES
ANCHO_VENTANA = 500
ALTO_VENTANA = 500
COLOR_BLANCO = (255,255,255)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = ( 0, 0,128)
#POSICIONES
posicion_circulo = [0, 100]
#TIMER
timer_segundos = pygame.USEREVENT #un evento que creo yo
#que este evento se ejecute con un tiempo que yo determine
#esto se va a ejecutar cada 1 segundo
pygame.time.set_timer(timer_segundos,1000) #1000 es 1 segundo
#crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
#Seteo un título en la pantalla
pygame.display.set_caption("Juego")
flag_correr = True
while flag_correr:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        #if evento.type == pygame.USEREVENT:   #si tengo mas de un timer
        if evento.type == timer_segundos:
            if (posicion_circulo[0] < ANCHO_VENTANA+80): #si esta contenido en la pantalla-radio
                posicion_circulo[0] = posicion_circulo[0] + 30 #cada segundo se mueve 10 pixeles
            else:
                posicion_circulo[0] = 0
    #fondo color
    pantalla.fill(COLOR_CELESTE)
    pygame.draw.circle(pantalla, COLOR_AMARILLO,posicion_circulo,80) #80 es el radio
    #pygame.draw.rect(pantalla, COLOR_BLANCO,(30,5,100,200)) #horizonta,vertical,ancho,alto
    #mostrar
    pygame.display.flip()
    #input()
pygame.quit()
