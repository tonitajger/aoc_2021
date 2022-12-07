import click
import numpy as np

from utils.input_parser import parse_lines




def parse_sheet(day, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        input_str = f.read()
    sheet_str, instructions_str = input_str.split('\n\n')
    sheet_coors = np.array([list(map(int, coor_str.split(','))) for coor_str in sheet_str.splitlines()])
    instructions = []
    for i in instructions_str.splitlines():
        ax, val = i.split()[-1].split('=')
        instructions.append((ax, int(val)))
    print(np.max(sheet_coors[:, 0]), np.max(sheet_coors[:, 1]))


    sheet = np.zeros((np.max(sheet_coors[:, 0]) + 1, np.max(sheet_coors[:, 1]) + 2), dtype=np.uint)
    for c in sheet_coors:
        sheet[tuple(c)] = 1
    
    return np.transpose(sheet), instructions 


def fold(sheet, instructions, only_first=False):
    if only_first:
        instructions = instructions[:1]

    
    for axis, val in instructions:
        print(axis, val)
        # print(sheet)
        if axis == 'y':
            if sheet.shape[0] % 2 == 1:
                mat1, _, mat2 = np.split(sheet, [val, val+1], axis=0)
            else:
                print('dafaq')
                mat1, mat2 = np.split(sheet, [val], axis=0)
            # print(mat1.shape, mat2.shape)

            sheet = np.flip(mat2, axis=0) + mat1


        elif axis == 'x':
            mat1, _, mat2 = np.split(sheet, [val, val+1], axis=1)
            # print(mat1.shape, mat2.shape)
            mat1 = np.pad(mat1, ((0, 0), (mat2.shape[0] - mat1.shape[0], 0)))
            sheet = np.flip(mat2, axis=1) + mat1

    return sheet


def part_1(sheet, instructions):
    sheet = fold(sheet, instructions, only_first=True)
    return np.sum(sheet > 0)
    

np.set_printoptions(threshold=np.inf)

def part_2(sheet, instructions):
    sheet = fold(sheet, instructions, only_first=False)
    visualize_sheet = np.empty(sheet.shape, dtype=str)
    print(sheet)
    for index, x in np.ndenumerate(sheet):
        if x > 0:
            visualize_sheet[index] = '#'
        else:
            visualize_sheet[index] = '.'
    
    for i in visualize_sheet:
        for j in i:
            print(j, end='')
        print()
                
    return visualize_sheet


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](*parse_sheet(13, example=example))) # Replace with day


if __name__ == '__main__':
    main()