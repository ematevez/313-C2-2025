import pygame

pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
reloj = pygame.time.Clock()
corriendo = True

fuente_arial = pygame.font.SysFont("Arial", 20)

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("hola")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("a")

    pantalla.fill("purple")

    #                                 (x, y, ancho, alto)
    pygame.draw.rect(pantalla, "red", (pantalla.get_width()/2 - 50, pantalla.get_height()/2 - 50, 100, 100))

    #                                     (x, y)
    """ pygame.draw.circle(pantalla, "green", (100, 100), 100) """
    


    texto = fuente_arial.render("Albi es la mejor tutora", True, "black")
    pantalla.blit(texto, (0, 500))


    pygame.display.flip()
    reloj.tick(60) #fps

pygame.quit()

print("hola")