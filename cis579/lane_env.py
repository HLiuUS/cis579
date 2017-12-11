"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
import time
import sys

# support for both Python 2.x and 3.x
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
LANE_H = 7  # grid height
LANE_W = 1  # grid width
MERGE_H = 1  # grid height
MERGE_W = 4  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(LANE_H * UNIT, MERGE_W * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=LANE_H * UNIT,
                           width=MERGE_W * UNIT)

        # create grids
        for c in range(0, (LANE_W + 1) * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, LANE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, LANE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, LANE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

	for c in range(0, MERGE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0 + 120, c, MERGE_H * UNIT + 120
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, (MERGE_H + 1) * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r + 120, MERGE_W * UNIT, r + 120
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # create oval
        oval_center = origin + UNIT * 3
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] + 225,
            origin[0] + 15, origin[1] + 255,
            fill='red')

        # pack all
        self.canvas.pack()


if __name__ == '__main__':
    env = Maze()
    env.mainloop()
