import pygame as pg

import resources


class Cell:
    def __init__(self, inactive):
        self.inactive = inactive
        self.flagged = False
        self.possibly_mine = False
        self.mine = False
        self.adjacent = 0
        self.cursor_above = False
        self.cell_dead = False

    def set_mine(self):
        self.mine = True

    def set_flag(self):
        if self.inactive:
            return
        if self.flagged:
            self.possibly_mine = True
            self.flagged = False
        elif self.possibly_mine:
            self.possibly_mine = False
            self.flagged = False
        else:
            self.flagged = True

    def is_mine(self):
        return self.mine

    def set_inactive(self, inactive):
        self.inactive = inactive

    def is_inactive(self):
        return self.inactive

    def set_num_of_adjacent(self, num):
        self.adjacent = num

    def draw(self, frame, rect, font):
        if not self.cell_dead:
            pg.draw.rect(frame, self.get_cell_color(), rect)
        elif self.mine:
            frame.blit(resources.Assets.bomb, rect)

        if self.flagged:
            frame.blit(resources.Assets.flag, rect)
        elif self.possibly_mine:
            frame.blit(resources.Assets.m_flag, rect)

        if self.adjacent > 0 and self.inactive and not self.mine:
            label = font.render(str(self.adjacent), 1, self.get_number_color(self.adjacent))
            frame.blit(label, self.center_text_in_cell(rect, label.get_rect()))
        if self.cursor_above:
            self.cursor_above = False

    def get_cell_color(self):
        if self.inactive:
            return pg.Color(resources.Colors.INACTIVE_CELL_COLOR)
        elif self.possibly_mine:
            return pg.Color(resources.Colors.POSSIBLY_MINE)
        elif self.cursor_above:
            return pg.Color(resources.Colors.CURSOR_ABOVE)
        return pg.Color(resources.Colors.ACTIVE_CELL_COLOR)

    @staticmethod
    def center_text_in_cell(rect, rect_l):
        return pg.Rect(rect.x + rect_l.width * 0.5, rect.y, rect.width, rect.height)

    @staticmethod
    def get_number_color(val):
        switcher = {
            1: pg.Color(resources.Colors.CELL_ADJACENT_1),
            2: pg.Color(resources.Colors.CELL_ADJACENT_2),
            3: pg.Color(resources.Colors.CELL_ADJACENT_3),
            4: pg.Color(resources.Colors.CELL_ADJACENT_4),
            5: pg.Color(resources.Colors.CELL_ADJACENT_5),
        }
        return switcher.get(val, pg.Color(resources.Colors.CELL_ADJACENT_5))
