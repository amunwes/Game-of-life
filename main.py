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
BLUE = (0, 0, 255)

WIDTH = 8
HEIGHT = 8
MARGIN = 1

X_DIM = 80
Y_DIM = 80

BTN_HEIGHT = 50


def init_grid(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    return cells


def update_life(surface, cur):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]

        if cur[r, c] == 1 and num_alive < 2 or num_alive > 3:
            col = col_almost_dead
        elif (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        # pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))
        pygame.draw.rect(surface, col,
                         (c * (WIDTH + MARGIN) + MARGIN, r * (WIDTH + MARGIN) + MARGIN, WIDTH, HEIGHT))

    return nxt


def update_grid(r, c, cells):
    if cells[r, c] == 1:
        cells[r, c] = 0
    else:
        cells[r, c] = 1

    return cells

# unused function for
def crawl(cells): # unused
    for r, c in np.ndindex(cells.shape):
        if cells[r, c]:
            if (0 <= r + 1 < X_DIM):
                update_grid(r + 1, c, cells)


def draw_grid(grid):
    for r, c in np.ndindex(grid.shape):
        if not grid[r, c]:
            pygame.draw.rect(screen, col_background,
                             (c * (WIDTH + MARGIN) + MARGIN, r * (WIDTH + MARGIN) + MARGIN, WIDTH, HEIGHT))
        else:
            pygame.draw.rect(screen, col_alive,
                             (c * (WIDTH + MARGIN) + MARGIN, r * (WIDTH + MARGIN) + MARGIN, WIDTH, HEIGHT))


if __name__ == '__main__':

    pygame.init()

    # Set the width and height of the screen [width, height]
    board = (MARGIN + X_DIM * (WIDTH + MARGIN), MARGIN + Y_DIM * (HEIGHT + MARGIN))
    size = (board[0], board[1] + BTN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Conway's game of Life")

    grid = init_grid(X_DIM, Y_DIM)
    # accompanying grid that tracks whether a cell has been swapped to keep from swapping at the frame rate
    swap_status = init_grid(X_DIM, Y_DIM)
    mouse_down = False

    # rendering text for buttons
    smallfont = pygame.font.SysFont('sans', 30)
    START = smallfont.render('START', True, WHITE)
    RESET = smallfont.render('RESET', True, WHITE)
    # rendering necessary rectangles
    btn_bg = pygame.Rect(0, MARGIN + Y_DIM * (HEIGHT + MARGIN), size[0], BTN_HEIGHT)
    reset_btn = pygame.Rect(0, MARGIN + Y_DIM * (HEIGHT + MARGIN), size[0] / 2, BTN_HEIGHT)
    start_btn = pygame.Rect(size[0] / 2, MARGIN + Y_DIM * (HEIGHT + MARGIN), size[0] / 2, BTN_HEIGHT)
    reset_btn.scale_by_ip(x=0.8, y=0.8)
    start_btn.scale_by_ip(x=0.8, y=0.8)

    # start and finish flags for controlling quitting and which loop runs.
    done = False
    start = False

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
                player_position = pygame.mouse.get_pos()
                if reset_btn.collidepoint(player_position):
                    grid = init_grid(X_DIM, Y_DIM)
                    start = False
                if start_btn.collidepoint(player_position):
                    start = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                swap_status = init_grid(X_DIM, Y_DIM)

        # --- Game logic should go here
        if mouse_down and not start:
            player_position = pygame.mouse.get_pos()
            if 0 < player_position[0] < board[0] and 0 < player_position[1] < board[1]:
                row = (player_position[1] - MARGIN) // (WIDTH + MARGIN)
                col = (player_position[0] - MARGIN) // (HEIGHT + MARGIN)
                if not swap_status[row, col]:
                    swap_status[row, col] = 1
                    grid = update_grid(row, col, grid)

        # --- Screen-clearing code goes here
        screen.fill(col_grid)

        # --- Drawing code should go here
        if start:
            grid = update_life(screen, grid)
        else:
            draw_grid(grid)
        # draw the buttons and assign text.

        pygame.draw.rect(screen, col_grid, btn_bg)
        pygame.draw.rect(screen, RED, reset_btn)
        pygame.draw.rect(screen, GREEN, start_btn)

        screen.blit(RESET, (reset_btn.topleft[0] + 100, reset_btn.topleft[1]))
        screen.blit(START, (start_btn.topleft[0] + 100, start_btn.topleft[1]))

        player_position = pygame.mouse.get_pos()
        pygame.draw.circle(screen, RED, (player_position[0], player_position[1]), 2)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.update()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
