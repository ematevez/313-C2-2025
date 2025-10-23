
'''
pygame.Rect() = función que representa ubicación y tamaño de un objeto y permite detectar 
si los Rect de 2 objetos se superponen (colisionan)
'''

import pygame
import colores


ANCHO_VENTANA = 500
ALTO_VENTANA = 500


pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("Mi primer Juego")


#imagen
imagen_rana = pygame.image.load("rana-sentada.jpg")#ancho, alto
imagen_rana = pygame.transform.scale(imagen_rana,(100,100))
#defino el área/superficie/rectángulo de mi imagen
                         #left, top, ancho, alto
rect_rana = pygame.Rect(30,100,101,101) #le doy 101 para que se vea


flag_correr = True
while flag_correr:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            #print(evento.pos)
            lista_posicion = list(evento.pos) #guardo la pos del click en 
                                                #una lista
            #print(lista_posicion)
            rect_rana[0] = lista_posicion[0] #modifico el left del rect
            rect_rana[1] = lista_posicion[1] #modifico el top del rect
            #print(rect_rana)


    pantalla.fill(colores.COLOR_CELESTE)
    #dibujar el rectangulo para ver cuanto ocupa
    pygame.draw.rect(pantalla, colores.RED1,rect_rana) 
    pantalla.blit(imagen_rana,rect_rana) #fundir la imagen en la ventana 
                               
    #mostrar los cambios de la pantalla
    pygame.display.flip()


pygame.quit()
