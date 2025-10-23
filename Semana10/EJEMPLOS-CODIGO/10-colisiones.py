import pygame
import colores

ANCHO_VENTANA = 500
ALTO_VENTANA = 500
flag_viva = True

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("Mi primer Juego")

#imagen
imagen_rana = pygame.image.load("rana-sentada.jpg")
                                                #ancho, alto
imagen_rana = pygame.transform.scale(imagen_rana,(100,100))
#defino el área/superficie/rectángulo de mi imagen
                    #left, top, ancho, alto
rect_rana = pygame.Rect(30,100,101,101) #le doy 101 para que se vea
#OTRA IMAGEN
imagen_mosca = pygame.image.load("mosca.png")
imagen_mosca = pygame.transform.scale(imagen_mosca,(50,50))

#tomo el rectangulo de la imagen cuando se construyó
rect_mosca = imagen_mosca.get_rect()
#puedo indicarle en que coordenadas lo quiero
rect_mosca.x = 300
rect_mosca.y = 300

flag_correr = True
while flag_correr:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            #print(evento.pos)
            lista_posicion = list(evento.pos) #guardo la pos del click en una lista
            #print(lista_posicion)
            rect_rana[0] = lista_posicion[0] #modifico el left del rect
            rect_rana[1] = lista_posicion[1] #modifico el top del rect
            #print(rect_rana)

    pantalla.fill(colores.COLOR_CELESTE)
    #RANA-dibujar el rectangulo para ver cuanto ocupa
    pygame.draw.rect(pantalla, colores.RED1,rect_rana)
    pantalla.blit(imagen_rana,rect_rana) #fundir la imagen en la ventana

    if rect_rana.colliderect(rect_mosca):
        flag_viva = False

    if flag_viva:
        #MOSCA-dibujar el rectangulo para ver cuanto ocupa
        pygame.draw.rect(pantalla, colores.RED1,rect_mosca)
        pantalla.blit(imagen_mosca,rect_mosca) #fundir la imagen en la ventana

    #mostrar los cambios de la pantalla
    pygame.display.flip()

pygame.quit()