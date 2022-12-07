import math

import click
import numpy as np
from PIL import Image


from matplotlib import cm


from utils.input_parser import parse_lines

frames = []
im_counter = 0
def take_image(im):
    # frames.append(Image.fromarray(np.uint8(cm.plasma(im)*255)).resize(np.multiply(im.shape, 3), resample=Image.NEAREST))
    frames.append(Image.fromarray(np.uint8(cm.plasma(im)*255)).resize(np.multiply(im.shape, 1), resample=Image.NEAREST))

import heapq

import click
import numpy as np

from utils.input_parser import parse_lines


class Grid:
    def __init__(self, mat):
        self.mat = mat
        self.shape = mat.shape
        self.grid = np.empty(mat.shape, dtype=Cell)
        self.low_points = []
        self.basins = []
        self.im_counter = 0

        for i, eli in enumerate(mat):
            for j, elj in enumerate(eli):
                self.grid[i][j] = Cell(elj, i, j)

        for i, eli in enumerate(self.grid):
            for j, cell in enumerate(eli):
                self._assign_neighbours(cell)
                
    
    def _assign_neighbours(self, cell):
        i, j = cell.coors
        m, n = self.shape

        if i - 1 >= 0:
            cell.neighbours.append(self.grid[i - 1][j])
        if i + 1 < m:
            cell.neighbours.append(self.grid[i + 1][j])
        if j - 1 >= 0:
            cell.neighbours.append(self.grid[i][j - 1])
        if j + 1 < n:
            cell.neighbours.append(self.grid[i][j + 1])


class Cell:
    def __init__(self, val, i, j) -> None:
        self.val = val
        self.distance = float('inf')
        self.previous = None
        self.coors = (i, j)
        self.neighbours = []
    
    def __str__(self):
        return f'{self.val}, {self.coors}, {self.neighbours}'


def parse_lines_to_matrix(lines):
    return np.array([list(map(int, list(l))) for l in lines])


def dijkstras(grid, im):
    start = grid.grid[0, 0]
    start.distance = start.val
    q = [start]
    visited = set()
    counter = 0
    while q:
        u = q.pop(0)
        visited.add(u.coors)
        im[u.coors] = u.val / 12
        if counter % 1000 == 0:
            take_image(im)
        counter += 1
        # if counter % 100 == 0:
        #     print(u.coors)
        for v in u.neighbours:
            if v.coors in visited:
                continue
            alt = u.distance + v.val
            if alt < v.distance:
                v.distance = alt
                v.previous = u
                q.append(v)
    take_image(im)


class PrioQueue(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        self.index = 0
        if initial:
            self._data = [(key(item), i, item) for i, item in enumerate(initial)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]

    def is_empty(self):
        return self._data == []


def dijkstras_h(grid, im):
    start = grid.grid[0, 0]
    start.distance = start.val
    q = PrioQueue(initial=[start], key=lambda x: x.distance)
    counter = 0
    visited = set()
    while not q.is_empty():
        u = q.pop()
        im[u.coors] = u.distance / 4000
        if counter % 1000 == 0:
            take_image(im)
            print(counter, u.distance)
        
        counter += 1
        visited.add(u.coors)

        for v in u.neighbours:
            if v.coors in visited:
                continue
            alt = u.distance + v.val
            if alt < v.distance:
                v.distance = alt
                v.previous = u
                q.push(v)

    take_image(im)


def get_path(node, im):
    path = []
    counter = 0
    while node.coors != (0, 0):
        im[node.coors] = 1

        if counter % 20 == 0:
            take_image(im)
        
        counter += 1

        path.append(node.val)
        node = node.previous
    
    im[node.coors] = 1
    take_image(im)
    return path


def expand_mat(mat):
    appended, incremented = mat, mat

    for i in range(2):
        for _ in range(4):
            incremented = incremented % 9 + 1
            appended = np.append(appended, incremented, i)

        appended, incremented = appended, appended

    return appended


def get_risk(mat, algo):
    grid = Grid(mat)
    im = np.zeros(mat.shape)
    algo(grid, im)
    end_node = grid.grid[-1, -1]
    path = get_path(end_node, im)
    return sum(path)


def part_1(lines, algo):
    return get_risk(parse_lines_to_matrix(lines), algo)
    

def part_2(lines, algo):
    return get_risk(expand_mat(parse_lines_to_matrix(lines)), algo)
    

@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(15, example=example), dijkstras_h))
    if frames:
        # Save GIF
        frames[0].save(
            'visualization/day15_risk_part_2_example.gif', 
            save_all=True,
            append_images=frames[1:], 
            optimize=False, 
            duration=[1] * (len(frames) - 1) + [1000],
            loop=0,
            subsampling=0,
            quality=100
        )

    
if __name__ == '__main__':
    main()
    