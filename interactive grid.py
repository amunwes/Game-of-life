import pygame
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

col_almost_dead = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)

width = 20
height = 20
margin = 5


def init_grid(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    return cells


def update_grid(r, c, cells):
    # row = (r - margin) // (width + margin)
    # col = (c - margin) // (height + margin)
    if cells[r, c] == 1:
        cells[r, c] = 0
    else:
        cells[r, c] = 1
    return cells


if __name__ == '__main__':

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (255, 255)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    grid = init_grid(10, 10)
    swap_status = init_grid(10, 10) # 2nd grid to map whether a square has been swapped this click
    mouse_down = False
    # grid[1,2] = 1

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                swap_status = init_grid(10, 10)

        # --- Game logic should go here
        if mouse_down:
            player_position = pygame.mouse.get_pos()
            row = (player_position[1] - margin) // (width + margin)
            col = (player_position[0] - margin) // (height + margin)
            if (not swap_status[row, col]):
                swap_status[row, col] = 1
                grid = update_grid(row, col, grid)

        # player_position = pygame.mouse.get_pos()
        # row = int(player_position[0] / ((width + margin) + margin))
        # col = int(player_position[1] / ((width + margin) + margin))
        # print(f'X?: {row}, \n Y?: {col}')

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        # --- Drawing code should go here

        for r, c in np.ndindex(grid.shape):
            if (not grid[r, c]):
                pygame.draw.rect(screen, WHITE,
                                 (c * (width + margin) + margin, r * (width + margin) + margin, width, height))
            else:
                pygame.draw.rect(screen, GREEN,
                                 (c * (width + margin) + margin, r * (width + margin) + margin, width, height))

        player_position = pygame.mouse.get_pos()
        pygame.draw.circle(screen, RED, (player_position[0], player_position[1]), 2)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
