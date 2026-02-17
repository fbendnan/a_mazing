import pygame


pygame.init()
DISPLAY_HEIGHT = 400
DISPLAY_WEIGHT = 400
screen = pygame.display.set_mode((DISPLAY_HEIGHT, DISPLAY_WEIGHT))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill((70,95,100))
        pygame.draw.rect(screen, (55, 20, 80), (50, 50, 100, 100))
        pygame.display.flip()
        

pygame.quit()