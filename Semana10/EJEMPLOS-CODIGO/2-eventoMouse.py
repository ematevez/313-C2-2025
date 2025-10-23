import pygame
#iniciar la pantalla
pygame.init() #lleva muchos parametros(no los daremos en detalle)
ANCHO_VENTANA = 500
ALTO_VENTANA = 500
COLOR_BLANCO = (255,255,255)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = ( 0, 0,128)
COLOR_AZUL = ( 0, 0, 255)
#POSICIONES
posicion_circulo = (100, 100)
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
        if evento.type == pygame.MOUSEBUTTONDOWN: #me trae la posicion del mouse
            print(evento.pos) #me muestra en 1 tupla el x,y de la posicion
            posicion_circulo = evento.pos  #ojo esto devuelve una tupla, si lo quiero
                                           #modificar, lo casteo a lista
    #fondo color
    pantalla.fill(COLOR_CELESTE)
    pygame.draw.circle(pantalla, COLOR_AMARILLO,posicion_circulo,80)
    #mostrar
    pygame.display.flip()
    #input()
pygame.quit()

