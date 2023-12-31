import pygame
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# color definitions
col_almost_dead = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

width = 8
height = 8
margin = 1

dimx = 100
dimy = 100

def update(surface, cur, sz):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r-1:r+2, c-1:c+2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_almost_dead
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        pygame.draw.rect(surface, col, (c*sz, r*sz, sz-1, sz-1))

    return nxt

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

def crawl(cells):
    for r, c in np.ndindex(cells.shape):
        if cells[r, c]:
            if (0 <= r+1 < dimx):
                update_grid(r+1, c, cells)

# def init(dimx, dimy): # eventually want to override with user input
#     cells = np.zeros((dimy, dimx))
#     # starting pattern/shape
#     pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
#     # starting position
#     pos = (3,3)
#     cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
#     return cells

def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("Conway's Game of Life")

    # cells = init(dimx, dimy)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        surface.fill(col_grid)
        cells = update(surface, cells, cellsize)
        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (dimx * width, dimy * height)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Conway's game of Life")

    grid = init_grid(dimx, dimy)
    swap_status = init_grid(dimx, dimy) # 2nd grid to map whether a square has been swapped this click
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
                swap_status = init_grid(dimx, dimy)

        # --- Game logic should go here
        if mouse_down:
            player_position = pygame.mouse.get_pos()
            row = (player_position[1] - margin) // (width + margin)
            col = (player_position[0] - margin) // (height + margin)
            if not swap_status[row, col]:
                swap_status[row, col] = 1
                grid = update_grid(row, col, grid)

        # crawl(grid)

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(col_grid)

        # --- Drawing code should go here
        for r, c in np.ndindex(grid.shape):
            num_alive = np.sum(grid[r - 1:r + 2, c - 1:c + 2]) - grid[r, c]

            if grid[r, c] == 1 and num_alive < 2 or num_alive > 3:
                col = col_almost_dead
            elif (grid[r, c] == 1 and 2 <= num_alive <= 3) or (grid[r, c] == 0 and num_alive == 3):
                grid[r, c] = 1
                col = col_alive

            col = col if grid[r, c] == 1 else col_background
            pygame.draw.rect(screen, col,
                         (c * (width + margin) + margin, r * (width + margin) + margin, width, height))

        player_position = pygame.mouse.get_pos()
        pygame.draw.circle(screen, RED, (player_position[0], player_position[1]), 2)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.update()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
