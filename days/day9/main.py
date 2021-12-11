import math

import click
import numpy as np
from PIL import Image


from matplotlib import cm


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

    def get_low_points(self):
        self.low_points = []
        for eli in self.grid:
            for cell in eli:
                if cell.val < min([n.val for n in cell.neighbours]):
                    self.low_points.append(cell)

        return self.low_points
    
    def get_basins(self):
        self.basins = []
        for lo in self.low_points:
            unchecked = [lo]
            checked = []
            while unchecked:
                cell = unchecked.pop()
                for n in cell.neighbours: 
                    if n.val > cell.val and n.val != 9:
                        unchecked.append(n)
  
                checked.append(cell)
            self.basins.append(set([c.coors for c in checked]))
        
        return self.basins


class Cell:
    def __init__(self, val, i, j) -> None:
        self.val = val
        self.coors = (i, j)
        self.neighbours = []
    
    def __str__(self):
        return f'{self.val}, {self.coors}, {self.neighbours}'


def parse_lines_to_matrix(lines):
    return np.array([list(map(int, list(l))) for l in lines])


def part_1(lines):
    mat = parse_lines_to_matrix(lines)
    grid = Grid(mat)
    return sum([p.val + 1 for p in grid.get_low_points()])


def part_2(lines):
    mat = parse_lines_to_matrix(lines)
    grid = Grid(mat)

    grid.get_low_points()
    basins = grid.get_basins()
    largest = sorted(list(map(len, basins)), reverse=True)[:3]

    return math.prod(largest)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Example input?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(9, example=example)))


if __name__ == '__main__':
    main()