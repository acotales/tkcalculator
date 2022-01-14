# -*- coding: utf-8 -*-

import tkinter as tk

from src.tkcalculator.calculator import Calculator


def example1():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


def example2():
    app = Calculator()
    app.start()


if __name__ == '__main__':
    example2()
