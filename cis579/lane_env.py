"""
Reinforcement learning maze example.

Red rectangle: lane player.
Yellow circle: merge palyer.

Accelarate: [reward = -1].
Decelarate: [reward = -1].
Maintain: [reward = +1].

Successful merge: [reward = +1000].
Collision: [reward = -10000].

This script is the environment part. The RL part is in RL_brain.py.

"""


import numpy as np
import time
import sys

# support for both Python 2.x and 3.x
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 80   # pixels
LANE_H = 7  # grid height
LANE_W = 1  # grid width
MERGE_H = 1  # grid height
MERGE_W = 4  # grid width


class Lane(tk.Tk, object):
    def __init__(self):
        super(Lane, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Lane')
        self.geometry('{0}x{1}'.format(MERGE_W * UNIT, LANE_H * UNIT))
        self._build_lane()

    def _build_lane(self):
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
            x0, y0, x1, y1 = c, 0 + 240, c, MERGE_H * UNIT + 240
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, (MERGE_H + 1) * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r + 240, MERGE_W * UNIT, r + 240
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([40, 40])

        # create oval
        oval_center = origin + UNIT * 3
        self.oval = self.canvas.create_oval(
            oval_center[0] - 30, oval_center[1] - 30,
            oval_center[0] + 30, oval_center[1] + 30,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 30, origin[1] + 450,
            origin[0] + 30, origin[1] + 510,
            fill='red')

        # pack all
        self.canvas.pack()


if __name__ == '__main__':
    env = Lane()
    env.mainloop()
