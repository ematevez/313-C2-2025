import pygame
#iniciar la pantalla
pygame.init()
#COLORES
ANCHO_VENTANA = 500
ALTO_VENTANA = 500
COLOR_BLANCO = (255,255,255)
COLOR_GRIS = (128, 128, 128)
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = ( 0, 0,128)
#POSICIONES
posicion_circulo = [0, 100]
posicion_imagen = [50,50]
#IMAGENES
imagen_rana = pygame.image.load("rana-sentada.jpg")
imagen_rana = pygame.transform.scale(imagen_rana,(150,150)) #puedo cambiar el tamaño de la imagen
#TEXTOS
fuente = pygame.font.SysFont("Arial", 30)
#el texto va a ser una superficie
texto = fuente.render("RANAG", True, COLOR_GRIS) #transforma el texto en una imagen
#el parametro True es Antialiasing elimina los bordes dentados de las imágenes 
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
            posicion_imagen = evento.pos #ojo que devuelve una tupla
            #si quiero modificar castear a lista

    
   #fondo color
    pantalla.fill(COLOR_CELESTE)
    #pygame.draw.rect(pantalla, COLOR_BLANCO,(30,60,100,200))
    pygame.draw.circle(pantalla, COLOR_AMARILLO,posicion_circulo,80)
    pantalla.blit(imagen_rana,posicion_imagen)  #fundir la imagen en la pantalla en las coordenadas
    pantalla.blit(texto,(300,300)) #fundir el texto en la pantalla

    #mostrar
    pygame.display.flip()
    #input()
pygame.quit()
