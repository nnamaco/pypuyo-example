import numpy as np
import sys
import tkinter as tk
from time import sleep
from math import floor
from random import choice
from copy import deepcopy


class Game:
    class _Puyo:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color

        def get_x(self):
            return self.x

        def get_y(self):
            return self.y

        def get_color(self):
            return self.color

        def set_x(self, val):
            self.x = val

        def set_y(self, val):
            self.y = val

    def __init__(self, width=5, height=13, frames_to_fall=1, types=("Red", "Blue", "Yellow", "Green", "Purple")):
        self.width = width
        self.height = (height + 2)
        self.board = np.full((self.height, self.width), None, dtype=object)
        self.next_spin = None
        self.next_move = None
        self.frames_to_fall = frames_to_fall
        self.frame_count = 1
        self.colors = types
        self.falling_puyos = (None, None)
        self.dirs_tf = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.dir_ = 2
        self.is_gameover = False
        self.highest_x = (self.width - 1)

    def is_over(self):
        return self.is_gameover

    def get(self):
        tmp_list = deepcopy(self.board)
        for puyo in self.falling_puyos:
            if puyo is not None:
                if (puyo.get_x() in range(self.width))\
                        and (puyo.get_y() in range(self.height)):
                    tmp_list[puyo.get_y()][puyo.get_x()] = puyo.get_color()
        return tmp_list[2:]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height-2

    def get_types(self):
        return self.colors

    def spin_left(self):
        self.next_spin = "l"

    def spin_right(self):
        self.next_spin = "r"

    def move_left(self):
        self.next_move = "l"

    def move_right(self):
        self.next_move = "r"

    def update(self):
        # spin
        if (self.next_spin is not None) and (None not in self.falling_puyos):
            center_x = self.falling_puyos[0].get_x()
            center_y = self.falling_puyos[0].get_y()
            dir_tf = (center_x - self.falling_puyos[1].get_x(),
                      center_y - self.falling_puyos[1].get_y()
                      )
            self.dir_ = self.dirs_tf.index(dir_tf)
            if self.next_spin == 'r':
                if self.dir_ >= 3:
                    self.dir_ = 0
                else:
                    self.dir_ += 1
            elif self.next_spin == 'l':
                if self.dir_ <= 0:
                    self.dir_ = 3
                else:
                    self.dir_ -= 1
            if ((center_x + self.dirs_tf[self.dir_][0]) in range(self.width))\
                    and ((center_y + self.dirs_tf[self.dir_][1]) in range(self.height))\
                    and ((self.board[center_y + self.dirs_tf[self.dir_][1]][center_x + self.dirs_tf[self.dir_][0]]) == None):
                self.falling_puyos[1].set_x(center_x + self.dirs_tf[self.dir_][0])
                self.falling_puyos[1].set_y(center_y + self.dirs_tf[self.dir_][1])
            self.next_spin = None
        # move
        if (self.next_move is not None) and (self.falling_puyos != (None, None)):
            no = [True, True]
            if self.next_move == 'r':
                add = 1
            elif self.next_move == 'l':
                add = -1
            for i, puyo in enumerate(self.falling_puyos):
                if puyo is not None:
                    puyo.set_x(puyo.get_x() + add)
                    if (puyo.get_x() in range(self.width)) and (self.board[puyo.get_y()][puyo.get_x()] == None):
                        no[i] = False
                else:
                    no[i] = False
            if True in no:
                for puyo in self.falling_puyos:
                    if puyo is not None:
                        puyo.set_x(puyo.get_x() - add)
            self.next_move = None
        # fall
        if self.frame_count == self.frames_to_fall:
            for i, puyo in enumerate(self.falling_puyos):
                if puyo is not None:
                    add = 0
                    if None not in self.falling_puyos:
                        if (self.dirs_tf[self.dir_][1] != 0)\
                                and (min(self.falling_puyos[0].get_y(), self.falling_puyos[1].get_y()) == puyo.get_y()):
                            add = 1
                    if ((puyo.get_y() + (add + 2)) <= self.height) and (self.board[puyo.get_y()+1][puyo.get_x()] == None):
                        puyo.set_y(puyo.get_y() + 1)
                    else:
                        # FIXME: Not shure if this works...
                        if puyo.get_y() <= -1:
                            self.is_gameover = True
                        if puyo.get_y() < self.highest_x:
                            self.highest_x = puyo.get_y()
                        self.board[puyo.get_y()][puyo.get_x()] = puyo.get_color()
                        tmp_list = list(self.falling_puyos)
                        tmp_list[i] = None
                        self.falling_puyos = tuple(tmp_list)
                        # puyo-disapearing
                        
            if self.falling_puyos == (None, None):
                self.falling_puyos = (self._Puyo(floor(self.width / 2), 1, choice(self.colors)),
                                 self._Puyo(floor(self.width / 2), 0, choice(self.colors))
                                 )
            self.frame_count = 1
        else:
            self.frame_count += 1


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        master.title('pyyo_beta')
        master.geometry("500x500")
        master.resizable(width=False, height=False)
        master.bind("<KeyPress>", lambda e: self.key_pressed(e.keysym))
        self.pack(expand=1, fill=tk.BOTH)

        self.game = Game(frames_to_fall=10)
        if max(self.game.get_height(), self.game.get_width()) == self.game.get_height():
            self.canvas = self.GameCanvas(self, 500 * (self.game.get_width() / self.game.get_height()), 500)
        elif max(self.game.get_height(), self.game.get_width()) == self.game.get_width():
            self.canvas = self.GameCanvas(self, 500, 500 * (self.game.get_height() / self.game.get_width()))
        else:
            self.canvas = self.GameCanvas(self, 500, 500)
        
        self.after(500, self.update)

    def update(self):
        self.game.update()
        self.canvas.draw_color(self.game.get())
        self.after(50, self.update)
    
    def key_pressed(self, key):
        if not self.game.is_over():
            if key == "a":
                self.game.move_left()
            elif key == "n":
                self.game.spin_left()
            elif key == "m":
                self.game.spin_right()
            elif key == "d":
                self.game.move_right()

    class GameCanvas(tk.Canvas):
        def __init__(self, master=None, width=100, height=100, x=0, y=0):
            self.width = width
            self.height = height
            super().__init__(master,
                             width=width,
                             height=height,
                             highlightthickness=0,
                             background="#FFFFFF"
                            )
            self.place(x=x, y=y)
        
        def draw_color(self, list):
            self.delete("all")
            block_width = max(self.height, self.width) / len(list)
            for yi in range(len(list)):
                for xi, color in enumerate(list[yi]):
                    if color is not None:
                        self.create_rectangle(block_width * xi,
                                            block_width * yi,
                                            block_width * (xi + 1),
                                            block_width * (yi + 1),
                                            fill=color,
                                            outline=color
                                            )


if __name__ == '__main__':
    root = tk.Tk()
    app = MainFrame(root)
    app.mainloop()