from dataclasses import dataclass

import pygame as pg

import resources


@dataclass
class Cell:
    """Klasa komórki na planszy."""
    inactive: bool = False
    flagged: bool = False
    possibly_mine: bool = False
    cursor_above: bool = False
    is_cell_dead: bool = False
    is_mine: bool = False
    adjacent: int = 0

    def set_flag(self):
        """ustawia flagę."""
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

    def draw(self, frame, rect, font, unlocked=False):
        """rysuje komórkę."""
        if not self.is_cell_dead:
            pg.draw.rect(frame, self.get_cell_color(unlocked), rect)
        elif self.is_mine:
            frame.blit(resources.Assets.bomb, rect)

        if self.flagged:
            frame.blit(resources.Assets.flag, rect)
        elif self.possibly_mine:
            frame.blit(resources.Assets.m_flag, rect)

        if self.adjacent > 0 and self.inactive and not self.is_mine:
            label = font.render(str(self.adjacent), 1, self.get_number_color(self.adjacent))
            frame.blit(label, self.center_text_in_cell(rect, label.get_rect()))
        if self.cursor_above:
            self.cursor_above = False

    def get_cell_color(self, unlocked):
        """zwraca kolor komórki w zależności od jej statusu."""
        if self.inactive:
            return pg.Color(resources.Colors.INACTIVE_CELL_COLOR)
        elif self.possibly_mine:
            return pg.Color(resources.Colors.POSSIBLY_MINE)
        elif self.cursor_above:
            return pg.Color(resources.Colors.CURSOR_ABOVE)
        elif unlocked and self.is_mine:
            return pg.Color(resources.Colors.CURSOR_ABOVE)
        return pg.Color(resources.Colors.ACTIVE_CELL_COLOR)

    @staticmethod
    def center_text_in_cell(rect, rect_l):
        """wyśrokowuje tekst."""
        return pg.Rect(rect.x + rect_l.width * 0.5, rect.y, rect.width, rect.height)

    @staticmethod
    def get_number_color(val):
        """zwraca kolor dla tekstu w zależności od
         tego jak wysoki jest numer (ilośc min w sąsiedzctwie)."""
        switcher = {
            1: pg.Color(resources.Colors.CELL_ADJACENT_1),
            2: pg.Color(resources.Colors.CELL_ADJACENT_2),
            3: pg.Color(resources.Colors.CELL_ADJACENT_3),
            4: pg.Color(resources.Colors.CELL_ADJACENT_4),
            5: pg.Color(resources.Colors.CELL_ADJACENT_5),
        }
        return switcher.get(val, pg.Color(resources.Colors.CELL_ADJACENT_5))
