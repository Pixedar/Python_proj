"""Moduł klasy ekran startowego"""
import tkinter as tk

import Assets as assets

MAX_BOARD_SIZE = 15
MIN_BOARD_SIZE = 2
DEFAULT_WIDTH = 7
DEFAULT_HEIGHT = 7
MAX_NUM_OF_BOMBS = 4


class MainWindow:
    """Klasa ekranu startowego"""

    def __init__(self):
        pass

    @staticmethod
    def validation_check(val, max_amount=None):
        """sprawdzanie poprwaności wprowadzanych danych"""
        if not val.get().isdigit():
            return False
        if (max_amount is not None and int(val.get()) < max_amount) or MIN_BOARD_SIZE <= int(
                val.get()) <= MAX_BOARD_SIZE:
            return True
        return False

    def callback(self, val, entry, max_amount=None):
        """ta metoda wykonuje się kiedy nastepuje zmiana wartości w entry"""
        if not self.validation_check(val, max_amount):
            entry.config({"background": assets.bad_val_color()})
        else:
            entry.config({"background": assets.correct_val_color()})

    @staticmethod
    def init_labels(frame):
        """inicjalizacja etykiet"""
        w_lab = tk.Label(frame, text='podaj szerokość: ')
        h_lab = tk.Label(frame, text='podaj wysokość: ')
        b_lab = tk.Label(frame, text='podaj ilość min: ')

        w_lab.grid(column=0, row=0)
        h_lab.grid(column=0, row=1)
        b_lab.grid(column=0, row=2)

    def init_entries(self, frame, width, height, amount):
        """inicjalizacja pół do wprowadzania tekstu"""
        w_entry = tk.Entry(frame, textvariable=width, width=4)
        h_entry = tk.Entry(frame, textvariable=height, width=4)
        bomb_entry = tk.Entry(frame, textvariable=amount, width=4)

        w_entry.grid(column=1, row=0)
        h_entry.grid(column=1, row=1)
        bomb_entry.grid(column=1, row=2)

        # inicjalizaja "śledzenia" zmian poszczególnych wartości
        width.trace("w", lambda name, index, mode, _width=width: self.callback(width, w_entry))
        height.trace("w", lambda name, index, mode, _height=height: self.callback(height, h_entry))

        max_b = int(width.get()) * int(height.get())
        amount.trace("w", lambda name, index,
                                 _mode, _amount=amount: self.callback(amount, bomb_entry, max_b))

    def init(self, button_callback):
        """metoda inicjalizująca"""
        frame = tk.Tk()

        width = tk.StringVar(value=DEFAULT_WIDTH)
        height = tk.StringVar(value=DEFAULT_HEIGHT)
        amount = tk.StringVar(value=MAX_NUM_OF_BOMBS)

        self.init_labels(frame)
        self.init_entries(frame, width, height, amount)

        start_button = tk.Button(frame, text='Start',
                                 command=lambda: button_callback(self, width, height, amount))

        start_button.grid_rowconfigure(0, weight=1)
        start_button.grid_columnconfigure(0, weight=1)
        start_button.grid(column=4, row=0, rowspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
        return frame
