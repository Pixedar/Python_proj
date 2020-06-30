from dataclasses import dataclass
import random

import pygame as pg
import tkinter
from tkinter import *
import ctypes

global bomb_entry
global w_entry
global h_entry
validationCheck = TRUE


class InvalidDataException:
    def __init__(self):
        super().__init__("Niepoprawne dane")

#ta funkcja wykonuje sie za każdym razem kiedy wpiszemy cos do pola
def callback(val, entry, max_amount=None):
    print(max_amount)
    global validationCheck
    if not val.get().isdigit():
        validationCheck = FALSE
        entry.config({"background": "Red"})
        raise InvalidDataException
    if (max_amount is None and 2 <= int(val.get()) <= 15) or (not max_amount is None and int(val.get()) < max_amount):
        validationCheck = TRUE
        entry.config({"background": "White"})
    else:
        validationCheck = FALSE
        entry.config({"background": "Red"})
        raise InvalidDataException


def initGUI():
    global bomb_entry
    global w_entry
    global h_entry

    frame = Tk()
    size_lab = Label(frame, text='podaj wymiary: ')
    size_lab_2 = Label(frame, text=' x ')
    #inicjlizacja zmiennych
    width = StringVar(value=7)
    height = StringVar(value=7)
    amount = StringVar(value=4)

    w_entry = Entry(frame, textvariable=width, width=4)
    #metoda trace umożliwia śledzenie zmian wartości zmiennej
    width.trace("w", lambda name, index, mode, width=width: callback(width, w_entry))

    h_entry = Entry(frame, textvariable=height, width=4)
    height.trace("w", lambda name, index, mode, height=height: callback(height, h_entry))
    #ustawianie pozycji elementów w gui
    size_lab.grid(column=0, row=0)
    w_entry.grid(column=1, row=0)
    size_lab_2.grid(column=2, row=0)
    h_entry.grid(column=3, row=0)

    bomb_num_lab = Label(frame, text='podaj ilość min: ')

    bomb_entry = Entry(frame, textvariable=amount, width=4)
    amount.trace("w", lambda name, index, mode, amount=amount: callback(amount, bomb_entry,
                                                                        int(width.get()) * int(height.get())))
    bomb_num_lab.grid(column=0, row=1)
    bomb_entry.grid(column=1, row=1)

    start_button = Button(frame, text='Start', command=handleButtonClick, padx=10, pady=10)

    start_button.grid(column=0, row=2)
    return frame


def handleButtonClick():
    if not validationCheck:
        ctypes.windll.user32.MessageBoxW(0, "Wprowadź poprawne dane", "Błąd", 1)



def main():
    # inicjalizacji gui
    okno = initGUI()

    okno.mainloop()
    pg.quit()


if __name__ == '__main__':
    main()
