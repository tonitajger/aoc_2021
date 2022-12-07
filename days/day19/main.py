import click
import numpy as np

from utils.input_parser import parse_lines


def parse_scanners(day, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        input_str = f.read()
    
    lines = [l.splitlines() for l in input_str.split('\n\n')]
    
    scanners = {}
    for l in lines:
        for el in l:
            if el.startswith('---'):
                scanner_id = int(el.split()[-2])
                scanners[scanner_id] = []
            else:
                beacon = np.array(list((map(int, el.split(',')))))
                scanners[scanner_id].append(beacon)
        
    return scanners


signs = [
    np.diag(np.array([1, 1, 1])),
    np.diag(np.array([1, -1, 1])),
    np.diag(np.array([1, 1, -1])),
    np.diag(np.array([1, -1, -1])),
    np.diag(np.array([-1, 1, 1])),
    np.diag(np.array([-1, -1, 1])),
    np.diag(np.array([-1, 1, -1])),
    np.diag(np.array([-1, -1, -1])),
]
shuffles = [
    np.array(
        [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]
    ),
    np.array(
        [[1, 0, 0],
         [0, 0, 1],
         [0, 1, 0]]
    ),
    np.array(
        [[0, 1, 0],
         [1, 0, 0],
         [0, 0, 1]]
    ),
    np.array(
        [[0, 1, 0],
         [0, 0, 1],
         [1, 0, 0]]
    ),
    np.array(
        [[0, 0, 1],
         [1, 0, 0],
         [0, 1, 0]]
    ),
    np.array(
        [[0, 0, 1],
         [0, 1, 0],
         [1, 0, 0]]
    ),
]
def compare(a, b, scanners):
    scanners[a]
    scanners[b]
    for sh in shuffles:
        # print(f"shuffle: {sh}")
        for si in signs:
            # print(f"sign: {si}")
            for sca in scanners[a]:
                for scb in scanners[b]:
                    matching = set()
                    
                    # print(np.matmul(np.matmul(sh, si), scb).shape)
                    diff = sca - np.matmul(np.matmul(sh, si), scb)
                    # print(sca, scb)
                    # print(b_coor)
                    matching.add((tuple(sca), tuple(scb)))

                    modded = set()
                    for scb_1 in scanners[b]:
                        mod = tuple(diff + np.matmul(np.matmul(sh, si), scb_1))
                        modded.add(mod)
                    
                    unmodded = set()
                    for sca_1 in scanners[a]:
                        unmodded.add(tuple(sca_1))

                    if len(modded.union(unmodded)) >= 12: 
                        print(len(modded.union(unmodded)))                 
                        return diff
    return None, None




def part_1(scanners):
    # return list(scanners.keys())
    diffs = {}
    checked = set()
    scanners_ids = list(scanners.keys())
    for i in scanners_ids:
        for j in scanners_ids:
            if i == j:
                continue
            print(i, j)

            if (i, j) in checked:
                continue 
            diff = compare(i, j, scanners)

            diffs[(i, j)] = diff
    
            print(diffs)



def part_2(lines):
    return


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_scanners(19, example=example))) # Replace with day


if __name__ == '__main__':
    main()