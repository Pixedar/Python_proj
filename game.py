"""Moduł okna gry saper"""

from dataclasses import dataclass
import random
import time

import pygame as pg

from cell import Cell
import resources

CELLS_SIZE = 18
CELL_MARGIN = 0.25
MOUSE_LEFT_CLICK_KEY_CODE = 1
MOUSE_RIGHT_CLICK_KEY_CODE = 3
SECRET_CODE = 'xyzzy'
WINDOW_TITLE = 'Saper'


# pylint: disable=R0201
class GameWindow:
    """Głowne okno gry."""

    def __init__(self, width, height, bombs):
        """Inicjalizuje: kontroler gry,pygmae oraz ustawia wielkość i tytuł okna."""
        pg.init()
        resources.Assets.load(CELLS_SIZE)
        self.frame = pg.display.set_mode(self.get_window_size(height, width))
        pg.display.set_caption(WINDOW_TITLE)
        self.game_controller = GameController(height, width, bombs)

    def start_game(self):
        """startuje grę."""
        self.game_controller.main_loop(self.frame)
        pg.quit()

    def get_window_size(self, width, height):
        """zwraca rozmiar okna zależny od wymiarów planszy oraz wielkości komórek."""
        margin = get_margin()
        size = CELLS_SIZE + margin
        return [size * height + margin, size * width + margin]


@dataclass
class GameController:
    """Klasa odpowiedzialna na kontrolowanie gry."""
    game_ended_time: int = 0
    game_ended: bool = False
    game_failed: bool = False
    secret_code_unlocked: bool = False

    def __init__(self, w, h, bombs):
        """Inicjalizuje klasę."""
        self.game_start_time = time.time()
        self.width = w
        self.height = h
        self.n_mines = bombs
        self.margin = get_margin()
        self.grid = self.get_grid()
        self.font = get_font()
        self.init_board()

    def init_board(self):
        """Dodaje miny do planszy i przypisuje liczbę min sąsiadujących dla każdej kómórki."""
        self.add_mines()
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.grid[x][y].adjacent = self.get_adjacency(x, y)

    def expand(self, x, y):
        """Odkrywa planszę."""
        for xi in range(max(0, x - 1), min(x + 2, self.width)):
            for yi in range(max(0, y - 1), min(y + 2, self.height)):
                cell = self.grid[xi][yi]
                if not cell.is_mine and not cell.flagged and not cell.possibly_mine:
                    if cell.adjacent == 0 and not cell.inactive:
                        cell.inactive = True
                        self.expand(xi, yi)
                    else:
                        cell.inactive = True

    def get_grid(self):
        """Zwraca macierz kmórek planszy."""
        grid = []
        for row in range(self.width):
            grid.append([])
            for column in range(self.height):
                grid[row].append(Cell())
        return grid

    def get_surrounding(self, x, y):
        """Zwraca sąsiadujące komórki"""
        result = []
        for xi in range(max(0, x - 1), min(x + 2, self.width)):
            for yi in range(max(0, y - 1), min(y + 2, self.height)):
                result.append(self.grid[xi][yi])
        return result

    def get_adjacency(self, x, y):
        """Zwraca ilość min."""
        positions = self.get_surrounding(x, y)
        n_mines = sum(1 if w.is_mine else 0 for w in positions)
        return n_mines

    def add_mines(self):
        """dodaje miny do planszy."""
        mines = []
        while len(mines) < self.n_mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (x, y) not in mines:
                self.grid[x][y].is_mine = True
                mines.append((x, y))

    def main_loop(self, frame):
        """Główna pętla to tutaj przechywywane są eventy i wywołuje się rysowanie poszczególnych klatek."""
        key_seq = []
        loop_status = True
        while loop_status:
            if self.check_game_status() and not self.game_ended:
                self.game_ended_time = time.time()
                self.game_ended = True

            pos = pg.mouse.get_pos()
            column = pos[0] // (CELLS_SIZE + self.margin)
            row = pos[1] // (CELLS_SIZE + self.margin)
            if row in range(0, self.width) and column in range(0, self.height):
                self.grid[row][column].cursor_above = True

            for event in pg.event.get():
                if event.type is pg.QUIT:
                    loop_status = False
                elif event.type is pg.MOUSEBUTTONDOWN:
                    self.update_cell_status(event, row, column)
                if event.type is pg.KEYDOWN:
                    key_seq.append(event.unicode)
                    if SECRET_CODE in ''.join(key_seq):
                        self.secret_code_unlocked = True
                        key_seq = []

            self.draw(frame)
            if self.game_ended:
                self.end_seq(frame)

            pg.display.flip()
        return loop_status

    def end_seq(self, frame):
        """Ta metoda pokazuje ekran końcowy w zależności od wyniku gry."""
        row = random.randint(0, self.width - 1)
        column = random.randint(0, self.height - 1)
        self.grid[row][column].is_cell_dead = True

        img = resources.Assets.win
        text = 'WYGRAŁEŚ w {} s'.format(round(self.game_ended_time - self.game_start_time))
        if self.game_failed:
            img = resources.Assets.death
            text = 'PRZEGRAŁEŚ !'

        window_size = frame.get_size()
        game_over_img = pg.transform.scale(img,
                                           (round(window_size[0] * 1), round(window_size[1] * 1)))
        frame.blit(game_over_img, game_over_img.get_rect())

        label = self.font.render(text, 2, pg.Color('white'))
        frame.blit(label, pg.Rect(round(window_size[0] * 0.5 - label.get_rect().width * 0.5),
                                  5, 200, 200), label.get_rect())

    def update_cell_status(self, event, row, column):
        """Aktualizacja statusu komórki (np oflagowanie komórki itd)."""
        if self.game_ended:
            return
        if not (row in range(0, self.width) and column in range(0, self.height)):
            return
        cell = self.grid[row][column]
        if event.button is MOUSE_LEFT_CLICK_KEY_CODE:
            if cell.flagged or cell.possibly_mine:
                return
            if cell.is_mine:
                self.game_ended = True
                self.game_failed = True
            cell.inactive = True
            self.expand(row, column)
        elif event.button is MOUSE_RIGHT_CLICK_KEY_CODE:
            cell.set_flag()

    def draw(self, frame):
        """Metoda rysująca planszę."""
        frame.fill(pg.Color(resources.Colors.BOARD_BACKGROUND))
        for row in range(self.width):
            for column in range(self.height):
                rect = self.get_cell_rect(row, column)
                cell = self.grid[row][column]
                cell.draw(frame, rect, self.font, self.secret_code_unlocked)

    def check_game_status(self):
        """Metoda sprawdzająca czy gracz wygrał."""
        flag_sum = 0
        inactive_sum = 0
        for row in range(self.width):
            for column in range(self.height):
                cell = self.grid[row][column]
                if cell.inactive:
                    inactive_sum = inactive_sum + 1
                if cell.flagged:
                    flag_sum = flag_sum + 1
        if self.n_mines is flag_sum and inactive_sum is self.width * self.height - self.n_mines:
            return True
        return False

    def get_cell_rect(self, row, column):
        """Zwraca krztałt (tutuaj kwadrat) który definuje komórkę na planszy."""
        size = CELLS_SIZE + self.margin
        rect_w = size * column + self.margin
        rect_h = size * row + self.margin
        return pg.Rect(rect_w, rect_h, CELLS_SIZE, CELLS_SIZE)


def get_margin():
    """Zwraca odstęp między komórkami w zależny od wielkości komórek."""
    return round(CELLS_SIZE * CELL_MARGIN)


def get_font():
    """Zwraca font."""
    return pg.font.SysFont(resources.Fonts.CELL_FONT, round(CELLS_SIZE * 1.5))
