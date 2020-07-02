import pygame as pg
from PyQt5.QtGui import *


class Assets:
    @staticmethod
    def load():
        Assets.bomb = QImage("./images/cross.png")
        Assets.flag = QImage("./images/flag.png")
        Assets.m_flag = QImage("./images/m_flag.png")


def bad_val_color():
    return '#c92508'


def main_window_font():
    return 'Helvetica 18 bold'


def correct_val_color():
    return 'white'
