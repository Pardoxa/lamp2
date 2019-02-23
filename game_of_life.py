#!/usr/bin/env python

# credit: https://raw.githubusercontent.com/pimoroni/unicorn-hat-hd/master/examples/game-of-life.py
import random
import time
from random import randint
import unicornhathd


try:
    xrange
except NameError:
    xrange = range


width, height = unicornhathd.get_shape()

size = width * height


class GameOfLife:
    def __init__(self):
        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]
        self.color = [[154, 154, 174], [0, 0, 255], [0, 0, 200], [0, 0, 160], [0, 0, 140], [0, 0, 90], [0, 0, 60], [0, 0, 0]]

    def random_new_live(self):
        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]

    def value(self, x, y):
        index = ((x % width) * height) + (y % height)
        return self.board[index]

    def neighbors(self, x, y):
        sum = 0
        for i in xrange(3):
            for j in xrange(3):
                if i == 1 and j == 1:
                    continue
                if self.value(x + i - 1, y + j - 1) == 0:
                    sum = sum + 1
        return sum

    def next_generation(self):
        new_board = [False] * size
        for i in xrange(width):
            for j in xrange(height):
                neigh = self.neighbors(i, j)
                lvl = self.value(i, j)
                if lvl == 0:
                    if neigh < 2:
                        new_board[i * height + j] = min(7, lvl + 1)
                    elif 2 <= neigh <= 3:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
                else:
                    if neigh == 3:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
        self.board = new_board

    def all_dead(self):
        for i in xrange(size):
            if self.board[i] != 7:
                return False
        return True

    def show_board(self):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                unicornhathd.set_pixel(i, j, rgb[0], rgb[1], rgb[2])
        unicornhathd.show()

def main(run, running):
    running(True)
    life = GameOfLife()

    while run():
        life.next_generation()
        life.show_board()
        if life.all_dead() or randint(0,1000) > 993:
            life.random_new_live()
        time.sleep(0.05)
    running(False)