import random

import pygame as pg

from cell import Cell
import resources

CELLS_SIZE = 18
CELL_MARGIN = 0.25

# pylint: disable=R0201
class GameController:
    def __init__(self, w, h, bombs):
        self.game_ended = False
        self.width = w
        self.height = h
        self.n_mines = bombs
        self.margin = self.get_margin()
        self.grid = self.get_grid()
        self.add_mines()
        self.last_cell = [0, 0]
        self.font = pg.font.SysFont(resources.Fonts.CELL_FONT, round(CELLS_SIZE * 1.5))
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.grid[x][y].set_num_of_adjacent(self.get_adjacency_n(x, y))

    def expand(self, x, y):

        pg.display.flip()

        for xi in range(max(0, x - 1), min(x + 2, self.width)):
            for yi in range(max(0, y - 1), min(y + 2, self.height)):
                cell = self.grid[xi][yi]
                if not cell.is_mine() and not cell.flagged and not cell.possibly_mine:
                    # print(self.grid[xi][yi].adjacent)
                    if cell.adjacent == 0 and not cell.is_inactive():
                        # print('ddsdfsfs')
                        cell.set_inactive(True)
                        self.expand(xi, yi)
                    else:
                        cell.set_inactive(True)

    def get_grid(self):
        grid = []
        for row in range(self.width):
            grid.append([])
            for column in range(self.height):
                grid[row].append(Cell(False))
        return grid

    def get_margin(self):
        return round(CELLS_SIZE * CELL_MARGIN)

    def get_surrounding(self, x, y):
        result = []
        for xi in range(max(0, x - 1), min(x + 2, self.width)):
            for yi in range(max(0, y - 1), min(y + 2, self.height)):
                result.append(self.grid[xi][yi])
        return result

    def get_adjacency_n(self, x, y):
        positions = self.get_surrounding(x, y)
        n_mines = sum(1 if w.is_mine() else 0 for w in positions)

        return n_mines

    def add_mines(self):
        mines = []
        while len(mines) < self.n_mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (x, y) not in mines:
                self.grid[x][y].set_mine()
                # w = self.grid.itemAtPosition(y,x).widget()
                # w.is_mine = True
                mines.append((x, y))

    def main_loop(self, frame):
        while True:

            pos = pg.mouse.get_pos()
            column = pos[0] // (CELLS_SIZE + self.margin)
            row = pos[1] // (CELLS_SIZE + self.margin)
            if row in range(0, self.width) and column in range(0, self.height):
                self.grid[row][column].cursor_above = True

            for event in pg.event.get():
                if event.type == pg.QUIT:  # If user clicked close
                    return True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.update_cell_status(event, row, column)

            self.draw(frame)
            if self.game_ended:
                self.end_seq(frame)
            pg.display.flip()

    def end_seq(self, frame):
        a = random.randint(0, self.width - 1)
        b = random.randint(0, self.height - 1)
        self.grid[a][b].cell_dead = True
        label = self.font.render('PRZEGRAŁEŚ !', 2, pg.Color(255, 255, 255))
        frame.blit(label, pg.Rect(0, 0, 200, 200), label.get_rect())

    def update_cell_status(self, event, row, column):
        if self.game_ended:
            return
        if not (row in range(0, self.width) and column in range(0, self.height)):
            return
        cell = self.grid[row][column]
        if event.button == 1:
            if cell.is_mine():
                self.game_ended = True
                self.last_cell = [row, column]
            cell.set_inactive(True)
            self.expand(row, column)
        elif event.button == 3:
            cell.set_flag()

    # def get_pos(self):
    #     pos = pg.mouse.get_pos()
    #     column = pos[0] // (CELLS_SIZE + self.margin)
    #     row = pos[1] // (CELLS_SIZE + self.margin)
    #     return row, column

    def draw(self, frame):
        frame.fill(pg.Color(resources.Colors.BOARD_BACKGROUND))

        size = CELLS_SIZE + self.margin
        # Draw the grid
        for row in range(self.width):
            for column in range(self.height):
                rect = self.get_cell_rect(row, column)
                cell = self.grid[row][column]
                cell.draw(frame, rect, self.font)

    def get_cell_rect(self, row, column):
        size = CELLS_SIZE + self.margin
        w = size * column + self.margin
        h = size * row + self.margin
        return pg.Rect(w, h, CELLS_SIZE, CELLS_SIZE)

    def get_pos(self):
        pos = pg.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = pos[0] // (CELLS_SIZE + self.margin)
        row = pos[1] // (CELLS_SIZE + self.margin)
        return [row, column]

# pylint: disable=R0201
class GameWindow:
    def __init__(self, w, h, bombs):
        pg.init()
        resources.Assets.load(CELLS_SIZE)
        self.frame = pg.display.set_mode(self.get_window_size(w, h))
        pg.display.set_caption("Saper")
        self.game_controller = GameController(w, h, bombs)

    def start_game(self):
        self.game_controller.main_loop(self.frame)
        pg.quit()

    def get_window_size(self, w, h):
        margin = self.get_margin()
        size = CELLS_SIZE + margin
        return [size * h + margin, size * w + margin]

    def get_margin(self):
        return round(CELLS_SIZE * CELL_MARGIN)

