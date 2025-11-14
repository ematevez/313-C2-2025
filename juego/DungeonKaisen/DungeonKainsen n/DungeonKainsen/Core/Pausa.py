import pygame                                     # pygame para fuentes y dibujo
# con p tenemos que poder acceder a un sub menu de pausa
class pausa:                                       # clase que representa el menú de pausa
    def __init__ (self, game):                     # recibe la instancia del juego para interactuar si hace falta
        self.game = game                            # referencia al juego
        self.font = pygame.font.SysFont("fancy", 36) # fuente para el título y opciones
        self.options = ["Reanudar", "Salir al Menu Principal"]  # opciones disponibles en el menú de pausa
        self.selected = 0                           # índice de la opción actualmente seleccionada

    def draw (self, screen):                        # dibuja la pantalla de pausa encima del juego
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # surface semitransparente para overlay
        overlay.fill((0, 0, 0, 180))                # rellena overlay con negro semi-transparente
        screen.blit(overlay, (0, 0))                # pinta overlay sobre toda la pantalla

        title = self.font.render("Pausa", True, (255, 255, 255))  # renderiza título "Pausa"
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))  # centra título horizontalmente

        for i, option in enumerate(self.options):   # dibuja cada opción del menú
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)  # resalta la opción seleccionada
            option_text = self.font.render(option, True, color)  # render del texto de la opción
            screen.blit(option_text, (screen.get_width() // 2 - option_text.get_width() // 2, 200 + i * 50))  # posiciona opción

    def boton_pausa(self, event):                   # método que intenta detectar tecla de pausa (no usado)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # si se presiona escape
            self.game.paused = not self.game.paused  # alterna estado de pausa