import pygame
from constants import *
from gamefield import *

def main():
    pygame.init()

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("BoomB0B")

    clock = pygame.time.Clock()
    done = False

    gf = gamefield(screen)

    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                done = True
            gf.handleEvent(event)

        screen.fill(GREEN)

        # Update gamefield and all of his objects
        gf.update()

        # Draw gamefield and all of his objects
        gf.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()