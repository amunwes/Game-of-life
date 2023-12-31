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


def update_cell(r, c, cells):
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
    size = (10*width+11*margin, 10*height+11*margin)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    grid = init_grid(10, 10)
    swap_status = init_grid(10, 10)  # 2nd grid to map whether a square has been swapped this click
    mouse_down = False

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
            if 0 < player_position[0] < size[0] and 0 < player_position[1] < size[1]:
                row = (player_position[1] - margin) // (height + margin)
                col = (player_position[0] - margin) // (width + margin)
                if not swap_status[row, col]:
                    swap_status[row, col] = 1
                    grid = update_cell(row, col, grid)

        # --- Screen-clearing code goes here

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        # --- Drawing code should go here

        for r, c in np.ndindex(grid.shape):
            if not grid[r, c]:
                pygame.draw.rect(screen, WHITE,
                                 (c * (width + margin) + margin, r * (height + margin) + margin, width, height))
            else:
                pygame.draw.rect(screen, GREEN,
                                 (c * (width + margin) + margin, r * (height + margin) + margin, width, height))

        player_position = pygame.mouse.get_pos()
        pygame.draw.circle(screen, RED, (player_position[0], player_position[1]), 2)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
