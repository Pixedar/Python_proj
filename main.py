import ctypes

import game as game
import start_window as m_window


class InvalidDataException:
    def __init__(self):
        super().__init__("Niepoprawne dane")


def start_button_callback(obj, w, h, amount):
    _max = int(w.get()) * int(h.get())
    if not obj.validation_check(w) and obj.validation_check(h) and obj.validation_check(amount, _max):
        ctypes.windll.user32.MessageBoxW(0, "Wprowadź poprawne dane", "Błąd", 1)
        raise InvalidDataException
    else:
        game.start(int(w.get()), int(w.get()), int(amount.get()))


def main():
    main_window = m_window.MainWindow()
    main_window.init(start_button_callback).mainloop()


if __name__ == '__main__':
    main()
