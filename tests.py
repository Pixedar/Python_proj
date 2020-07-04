import main
import unittest
import game
import resources
import start_window
import tkinter as tk
import pygame as pg

class MainTests(unittest.TestCase):
    def board_size_test(self):
        self.board_size_helper(1, 1, 1)
        self.board_size_helper(5, 1, 2)
        self.board_size_helper(4, 1, 2)
        self.board_size_helper(20, 500, 12)
        self.board_size_helper(5, 6, -4)
        self.board_size_helper(3, 3, 10)
        self.board_size_helper(3, 10, 5)

    def board_size_helper(self, w, h, b):
        main_window = start_window.MainWindow()
        width = tk.StringVar(value=w)
        height = tk.StringVar(value=h)
        amount = tk.StringVar(value=b)
        self.assertFalse(main.start_button_callback(main_window, width, height, amount))

class GameTest(unittest.TestCase):
    def cell_test_1(self):
        g = game.GameWindow(10,10,0)
        self.assertEqual(g.game_controller.get_adjacency(0,0),0)
    def cell_test_2(self):
        g = game.GameWindow(4, 4, 16)
        #g.start_game()
        event = pg.event.get()
        event.button = 1
        print(event.button)
        g.game_controller.update_cell_status(event,1,1)
        g.game_controller.update_cell_status(event, 1, 1)

class AssetsTest(unittest.TestCase):
    def file_test(self):
        resources.Assets.load()
        self.assertIsNotNone(resources.Assets.bomb)
        self.assertIsNotNone(resources.Assets.flag)
        self.assertIsNotNone(resources.Assets.m_flag)
        self.assertIsNotNone(resources.Assets.death)
        self.assertIsNotNone(resources.Assets.win)

# main_test = MainTests()
# main_test.board_size_test()