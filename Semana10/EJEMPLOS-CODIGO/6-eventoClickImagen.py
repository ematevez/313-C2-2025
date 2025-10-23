import pygame
#iniciar la pantalla
pygame.init()
#COLORES
ANCHO_VENTANA = 500
ALTO_VENTANA = 500
COLOR_CELESTE = ( 0, 0,128)
#POSICIONES
posicion_rana = [30, 100]
#IMAGENES
imagen_rana = pygame.image.load("rana-sentada.jpg")
imagen_rana = pygame.transform.scale(imagen_rana,(80,80)) #puedo cambiar el tamaño de la imagen

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
        if evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento.pos)
            posicion_rana = evento.pos

    #fondo color
    pantalla.fill(COLOR_CELESTE)
    pantalla.blit(imagen_rana,(posicion_rana),)  #fundir la imagen en una superficie

    #mostrar
    pygame.display.flip()
pygame.quit()
