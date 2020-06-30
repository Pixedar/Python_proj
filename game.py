from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ctypes

import random


bomb_img = QImage("./images/cross.png")
flag_img = QImage("./images/flag.png")
img_m_flag = QImage("./images/m_flag.png")

r_1 = 0
r_2 = 1

flagCtn = 0
num_of_bombs = 0
class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    fixed_size = 20
    def __init__(self, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)
        self.setFixedSize(QSize(self.fixed_size, self.fixed_size))
        self.flagCtn = 0
        self.x = x
        self.y = y
        self.stop = False

    def reset(self):
        self.is_start = False
        self.stat = False
        self.next_to_n = 0

        self.is_revealed = False
        self.is_flagged = False
        self.m_flagged = False
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.stat:
                p.drawPixmap(r, QPixmap(bomb_img))
                if not self.stop:
                    ctypes.windll.user32.MessageBoxW(0, "Przegrałeś", "Komunikat", 1)
                self.stop = True

            elif self.next_to_n > 0:
                pen = QColor('#f44336')
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.next_to_n))

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(flag_img))
        elif self.m_flagged:
            p.drawPixmap(r, QPixmap(img_m_flag))


    def update_flag(self):
        global flagCtn
        if (self.is_flagged):
            self.m_flagged = True
            self.is_flagged = False
            flagCtn = flagCtn - 1
        elif self.m_flagged:

            self.m_flagged = False
            self.is_flagged = False
            flagCtn = flagCtn - 1

        else:
            self.is_flagged = True
            flagCtn = flagCtn + 1
            if(flagCtn >= num_of_bombs):
               ctypes.windll.user32.MessageBoxW(0, "Wygrałeś", "Komunikat", 1)
        self.update()
        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.next_to_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        if (e.button() == Qt.RightButton and not self.is_revealed):
            print('d')
            self.update_flag()

        elif (e.button() == Qt.LeftButton):
            self.click()


class Game(QMainWindow):
    spacing = 4
    def setSpacing(self,spacing):
        self.spacing = spacing
    def setParams(self,w_size, h_size, num_of_mines):
        self.w_size = w_size
        self.h_size = h_size
        self.n_mines = num_of_mines

    def setLayout(self,*args, **kwargs):
        w = QWidget()
        hb = QHBoxLayout()

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(self.spacing)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

    def __init__(self, w_size, h_size, num_of_mines, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.setParams(w_size, h_size, num_of_mines)
        self.setLayout(*args, **kwargs)

        self.init_map()
        self.update_status(r_1)
        self.map_reset()
        self.update_status(r_1)
        self.show()

    def init_map(self):
        for x in range(0, self.w_size):
            for y in range(0, self.h_size):
                w = Pos(x, y)
                self.grid.addWidget(w, y, x)
                w.expandable.connect(self.expand_reveal)

    def get_neighboring_n(self,x, y):
        positions = self.get_neighboring(x, y)
        n_mines = sum(1 if w.stat else 0 for w in positions)

        return n_mines

    def set_mines(self):
        positions = []
        while len(positions) < self.n_mines:
            x, y = random.randint(0, self.w_size - 1), random.randint(0, self.h_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.stat = True
                positions.append((x, y))
    def set_nums(self):
        for x in range(0, self.w_size):
            for y in range(0, self.h_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.next_to_n = self.get_neighboring_n(x, y)

    def map_reset(self):
        for x in range(0, self.w_size):
            for y in range(0, self.h_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        self.set_mines()
        self.set_nums()

    def get_neighboring(self, x, y):
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.w_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.h_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def button_pressed(self):
        self.show_map()

    def show_map(self):
        for x in range(0, self.w_size):
            for y in range(0, self.h_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.w_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.h_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.stat:
                    w.click()

    def update_status(self, status):
        self.status = status


def start(w, h, amount):
    app = QApplication([])
    global num_of_bombs
    num_of_bombs = amount
    window = Game(w, h, amount)

    app.exec_()
