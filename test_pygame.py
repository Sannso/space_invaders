import pygame

pygame.init()
ventana = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Probando PyGame")

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

pygame.quit()