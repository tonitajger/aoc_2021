from collections import Counter

import click

from parse import lines_to_coor_pair
from utils.input_parser import parse_lines


def count_overlaps(lines, only_hv=False):
    pairs = lines_to_coor_pair(lines)
    if only_hv:
        pairs = [p for p in pairs if p.is_horizontal_or_vertical]

    all_coors = [coor for p in pairs for coor in p.get_all_coors()]
    cnt = Counter(all_coors)

    return len([p for p, c in cnt.items() if c > 1])


def part_1(lines):
    return count_overlaps(lines, only_hv=True)


def part_2(lines):
    return count_overlaps(lines)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, prompt='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(5, example=example)))


if __name__ == '__main__':
    main()
