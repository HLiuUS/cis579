# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 22:28:03 2017

@author: heng
"""

import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=3, ncols=3)

for i, ax in enumerate(axes.flat, start=1):
    action1 = ['decelerate', 'maintain', 'accelerate'][(i - 1)/3]
    action2 = ['decelerate', 'maintain', 'accelerate'][(i - 1)%3]
    temp = []
    for q_table in q_table_start_position_1:
        temp.append(q_table.loc[action1, action2])
    x, y =range(len(temp)), temp
    line, = ax.plot(x, y)
    ax.set_title('({}, {})'.format(action1, action2))
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Q Value')

fig.tight_layout()

fig.savefig('nashq.png', dpi=1200)
