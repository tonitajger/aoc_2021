import math

import click
import numpy as np
from PIL import Image


from matplotlib import cm


from utils.input_parser import parse_lines

frames = []
im_counter = 0
def take_image(im):
    frames.append(Image.fromarray(np.uint8(cm.plasma(im)*255)).resize((1024,1024)))


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

    def get_low_points(self, im=None):
        self.low_points = []
        for eli in self.grid:
            for cell in eli:
                if cell.val < min([n.val for n in cell.neighbours]):
                    self.low_points.append(cell)
                    if im is not None:
                        self.im_counter += 1
                        im[cell.coors] = cell.val / 9
                        if self.im_counter % 10 == 0:
                            take_image(im)
        return self.low_points
    
    def get_basins(self, im=None):
        self.basins = []
        for lo in self.low_points:
            unchecked = [lo]
            checked = []
            while unchecked:
                cell = unchecked.pop()
                for n in cell.neighbours: 
                    if n.val > cell.val and n.val != 9:
                        unchecked.append(n)
                        if im is not None:
                            self.im_counter += 1
                            im[n.coors] = n.val / 9
                            if self.im_counter % 500 == 0:
                                take_image(im)
                checked.append(cell)
            self.basins.append(set([c.coors for c in checked]))
        
        if im is not None:
            take_image(im)
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


def part_2(lines):
    mat = parse_lines_to_matrix(lines)
    grid = Grid(mat)


    im_array = np.ones(mat.shape)
    # im = Image.fromarray(np.uint8(cm.plasma(im_array/9)*255))
    # im.show()
    grid.get_low_points(im=im_array)
    # print(frames)
    basins = grid.get_basins(im=im_array)
    largest = sorted(list(map(len, basins)), reverse=True)[:3]

    if frames:
        # Save GIF
        frames[0].save(
            'visualization/day9_basin_animation.gif', 
            save_all=True,
            append_images=frames[1:], 
            optimize=False, 
            duration=[1] * (len(frames) - 1) + [1000],
            loop=0
        )

    return math.prod(largest)


def main():
    print(part_2(parse_lines(9)))


if __name__ == '__main__':
    main()