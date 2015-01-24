import pygame
from constants import *
from gamefield import *

def main():
    pygame.init()

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("BoomB0B")

    clock = pygame.time.Clock()
    done = False

    gf = gamefield()

    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()