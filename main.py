import ctypes

from game import GameWindow
import start_window as m_window

import tests
def start_button_callback(obj, w, h, amount):
    _max = int(w.get()) * int(h.get())
    if not (obj.validation_check(w) and obj.validation_check(h) and obj.validation_check(amount, _max)):
        ctypes.windll.user32.MessageBoxW(0, "Wprowadź poprawne dane", "Błąd", 1)
        return False
    else:
        obj.exit()
        game = GameWindow(int(w.get()), int(w.get()), int(amount.get()))
        game.start_game()
        return True


def main():
    main_window = m_window.MainWindow()
    main_window.init(start_button_callback).mainloop()
    # main_test = tests.GameTest()
    # main_test.cell_test_2()

if __name__ == '__main__':
    main()
