import click

from utils.input_parser import parse_lines

import numpy as np                                                               
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def str_to_int_list(input_str):
    return list(map(int, input_str[0].split(',')))


lines = parse_lines(6)
DAYS = 10


class Fishes:
    def __init__(self) -> None:
        self.fishes = init_fishes([0] * 9)
        

def init_fishes(fishes):
    for fish in str_to_int_list(lines):
        fishes[fish] += 1
    return fishes

FISHES = Fishes()

def get_fishes(i):
    fishes = FISHES.fishes
    xs = np.arange(len(fishes)) 
    width = 1
    plt.clf()
    bar = plt.bar(xs, fishes, width, align='center')
    plt.ylim((0, 1e5))

    new_fishes = fishes[1:] + [fishes[0]]
    new_fishes[6] += fishes[0]

    FISHES.fishes = new_fishes
    return bar


fig,ax = plt.subplots()

def main():
    ani = FuncAnimation(fig, get_fishes, interval=40, blit=True, repeat=True, frames=80)    
    ani.save("visualization/day6_fishes.gif", dpi=300, writer=PillowWriter(fps=5))


if __name__ == '__main__':
    main()
