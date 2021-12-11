import click
import numpy as np


from utils.input_parser import parse_lines


def parse_grid(lines):
    grid = [[int(d) for d in l] for l in lines]
    return np.array(grid)


def flash_cell(i, j, grid):
    grid[i-1:i+2, j-1:j+2] += 1


def flash_grid(grid):

    flashed = set()
    m, n = grid.shape
    changed = True
    while changed:
        changed = False
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if grid[i, j] >= 10 and (i, j) not in flashed:
                    changed = True
                    grid[i-1:i+2, j-1:j+2] += 1
                    flashed.add((i, j))
    
    for i, j in flashed:
        grid[i, j] = 0
    
    return len(flashed)


def part_1(lines):
    grid = np.pad(parse_grid(lines), 1)
    total_flashed = 0
    for i in range(100):
        grid += 1
        total_flashed += flash_grid(grid)
    
    return  total_flashed


def part_2(lines):
    grid = np.pad(parse_grid(lines), 1)
    counter = 1
    while True:
        grid += 1
        flash_grid(grid)
        if np.sum(grid[1:-1, 1:-1]) == 0:
            return counter
        counter += 1


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(11, example=example))) # Replace with day


if __name__ == '__main__':
    main()