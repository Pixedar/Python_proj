

from dataclasses import dataclass
import random

import pygame as pg
import tkinter
from tkinter import *


def callback(val, entry):
    if val.get().isdigit() and 0 < int(val.get()) < 100:
        entry.config({"background": "White"})
    else:
        entry.config({"background": "Red"})
    print(val.get())


def initGUI():
    frame = Tk()
    size_lab = Label(frame, text='podaj wymiary: ')
    size_lab_2 = Label(frame, text=' x ')
    width = StringVar(value=0)
    height = StringVar(value=0)
    amount = StringVar(value=0)

    w_entry = Entry(frame, textvariable=width, width=4)
    width.trace("w", lambda name, index, mode, width=width: callback(width, w_entry))

    h_entry = Entry(frame, textvariable=height, width=4)
    height.trace("w", lambda name, index, mode, height=height: callback(height, h_entry))
    size_lab.grid(column=0, row=0)
    w_entry.grid(column=1, row=0)
    size_lab_2.grid(column=2, row=0)
    h_entry.grid(column=3, row=0)

    bomb_num_lab = Label(frame, text='podaj ilość min: ')

    bomb_entry = Entry(frame, textvariable=amount, width=4)
    amount.trace("w", lambda name, index, mode, amount=amount: callback(amount, bomb_entry))
    bomb_num_lab.grid(column=0, row=1)
    bomb_entry.grid(column=1, row=1)

    start_button = Button(frame, text='Start', command=lambda: graj(width, height, amount), padx=10, pady=10)
    start_button.grid(column=0, row=2)

    return frame


def handleGame(width, height, amount):
    return True


def main():
    okno = initGUI()

    okno.mainloop()
    pg.quit()


if __name__ == '__main__':
    main()