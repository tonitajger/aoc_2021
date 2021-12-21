import copy

import click
import numpy as np

from utils.input_parser import parse_lines


class DeterministicDice:
    def __init__(self) -> None:
        self.current = 0
        self.num_rolls = 0
    
    def roll(self):
        old = self.current
        
        new = old
        rolls = []
        for _ in range(3):
            new = new % 100 + 1
            rolls.append(new)
        
        self.current = new
        self.num_rolls += 3
        return sum(rolls)


def part_1(lines):
    start_1, start_2 = [int(l.split()[-1]) for l in lines]
    dice = DeterministicDice()
    points = [0, 0]
    positions = [start_1, start_2]
    while True:
        for i in range(len(positions)):
            steps = dice.roll()
            new_pos = (positions[i] + steps - 1) % 10 + 1
            points[i] += new_pos
            positions[i] = new_pos
            if points[0] >= 1000 or points[1] >= 1000:
                return min(points) * dice.num_rolls


factor = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

seen = {}


def dirac_roll_start(start):

    points = [0, 0]
    positions = start

    sum = np.array([0, 0])
    for i in range(3, 10):
        new_roll = i
        sum += dirac_roll(points, positions, new_roll, 0, 0) * factor[i]
    return sum


def dirac_roll(points, positions, roll, player, counter):
    new_pos = (positions[player] + roll - 1) % 10 + 1
    
    # Blabla trying to be immutable
    new_points = copy.deepcopy(points)
    new_points[player] += new_pos
    new_positions = copy.deepcopy(positions)
    new_positions[player] = new_pos

    if new_points[player] >= 21:
        sums = np.array([0, 0])
        sums[player] = 1
        seen[(*points, *positions, player)] = sums
        return sums


    sums = np.array([0, 0])
    if (*new_points, *new_positions, 1 - player) in seen:
        sums = seen[(*new_points, *new_positions, 1 - player)]
    else:
        for i in range(3, 10):
            new_roll = i
            sums += dirac_roll(new_points, new_positions, new_roll, 1 - player, counter + 1) * factor[i]

        seen[(*new_points, *new_positions, 1 - player)] = sums

    return sums
        

def part_2(lines):
    start = [int(l.split()[-1]) for l in lines]
    return max(dirac_roll_start((start)))


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(21, example=example))) # Replace with day


if __name__ == '__main__':
    main()