import pygame
pygame.init()

# Inicializar el mixer
pygame.mixer.init()

# Cargar un sonido WAV
sonido_disparo = pygame.mixer.Sound("w_pistol.wav")

# Reproducir el sonido
sonido_disparo.play()

# Esperar unos segundos para escucharlo
pygame.time.wait(1000)
