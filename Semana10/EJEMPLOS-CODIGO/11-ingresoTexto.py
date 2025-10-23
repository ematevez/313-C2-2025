import pygame
from colores import *
#iniciar la pantalla
pygame.init()
#declarar constantes
ANCHO_VENTANA = 500
ALTO_VENTANA = 500

#crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
#Seteo un título en la pantalla
pygame.display.set_caption("Juego")

#Ingreso de texto del usuario
font_input = pygame.font.SysFont("Arial", 30)
ingreso = ""
ingreso_rect = pygame.Rect(100,200,150,40)


#El juego corre mientras el flag es true
flag_correr = True
while flag_correr:
    #guardo los eventos de la ventada en una lista
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        #Si el tipo de evento es salir (detecta si el usuario cierra la ventana)
        if evento.type == pygame.QUIT:
            flag_correr = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            else:
                ingreso += evento.unicode



    #pongo un fondo de color //fondo color
    pantalla.fill(COLOR_CELESTE)
    pygame.draw.rect(pantalla, ALICEBLUE, ingreso_rect , 2)
    #MUESTRO LA CAJA DE TEXTO PARA QUE INGRESE UN TEXTO
    font_input_surface = font_input.render(ingreso, True, BLACK) 
    pantalla.blit(font_input_surface, ( ingreso_rect.x+5 , ingreso_rect.y + 5 ))

    #mostrar los cambios en la pantalla
    pygame.display.flip()
#termina el programa
pygame.quit()  
