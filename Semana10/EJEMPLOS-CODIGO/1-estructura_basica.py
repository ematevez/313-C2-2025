import pygame
#iniciar la pantalla
pygame.init()
#declarar constantes
ANCHO_VENTANA = 500
ALTO_VENTANA = 500
COLOR_BLANCO = (255,255,255)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = ( 0, 0,128)
COLOR_AZUL = ( 0, 0, 255)
#crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
#Seteo un título en la pantalla
pygame.display.set_caption("Juego")
#El juego corre mientras el flag es true
flag_correr = True
while flag_correr:
    #guardo los eventos de la ventada en una lista
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        #Si el tipo de evento es salir (detecta si el usuario cierra la ventana)
        if evento.type == pygame.QUIT:
            flag_correr = False
    #pongo un fondo de color //fondo color
    pantalla.fill(COLOR_CELESTE)
    #dibujo un circulo de color
    pygame.draw.circle(pantalla, COLOR_AMARILLO,(100,100),80)
    #dibujo un rectangulo de color
    pygame.draw.rect(pantalla, COLOR_BLANCO,(30,60,100,200))
    #mostrar los cambios en la pantalla
    pygame.display.flip()
#termina el programa
pygame.quit()  
