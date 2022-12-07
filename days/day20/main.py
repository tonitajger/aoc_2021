import click

import numpy as np
import tqdm


def array2int(x):
    y = 0
    for i, j in enumerate(x[::-1]):
        y += j<<i
    return y


def parse_input(day, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        input_str = f.read()
    
    algo_str, mat_str = input_str.split('\n\n')

    algo = np.where(np.array(list(algo_str)) == '#', 1, 0)

    str_grid = np.array([list(row) for row in mat_str.split('\n')[:-1]])

    grid = np.where(str_grid == '#', 1, 0)

    return algo, grid


def iterate(algo, input_grid):
    m, n = input_grid.shape
    
    padded = input_grid
    # padded = np.pad(input_grid, (100, 100))
    # print(padded)
    new_grid = np.zeros(padded.shape, dtype=int)
    for (i, j), el in np.ndenumerate(padded[1:-1, 1:-1]):
        bin_list = padded[i:i+3, j:j+3].flatten()
        #print(padded.shape,(i,j))
        #print(padded[i:i+3, j:j+3].shape)
        idx = array2int(bin_list)
        # print((i,j), idx, algo[idx])
        new_grid[i+1, j+1] = algo[idx]

    return new_grid
    # 5285


def iterate_n(algo, mat, n):
    
    mat = np.pad(mat, (100, 100))
    for i in tqdm.tqdm(range(n)):
        mat = iterate(algo, mat)
        mat = mat[1:-1, 1:-1]
    return mat


def part_1(algo, grid):

    grid = iterate_n(algo, grid, 2)
    # grid_str = np.where(grid == 1, '#', '.')
    # print(grid_str)
    return np.sum(grid)


def part_2(algo, grid):
    grid = iterate_n(algo, grid, 50)
    # grid_str = np.where(grid == 1, '#', '.')
    # print(grid_str)
    return np.sum(grid)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    np.set_printoptions(threshold=np.inf)
    print(globals()['part_' + part](*parse_input(20, example=example))) # Replace with day


if __name__ == '__main__':
    main()