import pygame as pg

class Colors:
    BAD_VAL = '#c92508'
    CORRECT_VAL = 'white'
    BOARD_BACKGROUND = '#303030'
    ACTIVE_CELL_COLOR = 'white'
    INACTIVE_CELL_COLOR = '#5e5e5e'
    POSSIBLY_MINE = '#e6b027'
    CURSOR_ABOVE = '#c9c3c3'
    CELL_ADJACENT_1 = '#788dff'
    CELL_ADJACENT_2 = '#83ff78'
    CELL_ADJACENT_3 = '#fffd78'
    CELL_ADJACENT_4 = '#ffd078'
    CELL_ADJACENT_5 = '#ff3636'
class Fonts:
    MAIN_WINDOW_FONT = 'Helvetica 18 bold'
    CELL_FONT = "Roboto"
class Assets:
    @staticmethod
    def load(cell_size):
        Assets.bomb = pg.image.load("./images/bomb.png")
        Assets.flag = pg.image.load("./images/flag.png")
        Assets.m_flag = pg.image.load("./images/m_flag.png")
        Assets.flag = pg.transform.scale(Assets.flag,(cell_size,cell_size))
        Assets.m_flag = pg.transform.scale(Assets.m_flag, (cell_size, cell_size))
        Assets.bomb = pg.transform.scale(Assets.bomb, (cell_size, cell_size))