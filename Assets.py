import pygame as pg
from PyQt5.QtGui import *


class Assets:
    @staticmethod
    def load():
        Assets.bomb = QImage("./images/cross.png")
        Assets.flag = QImage("./images/flag.png")
        Assets.m_flag = QImage("./images/m_flag.png")