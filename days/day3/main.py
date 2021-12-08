import click
from collections import Counter

from utils.input_parser import parse_lines


def bin_to_dec(bin_str):
    return int(bin_str, 2)


def part_1(lines):
    counts = []
    for line in lines:
        for i, c in enumerate(line):
            if len(counts) < i + 1:
                counts.append(Counter())
            counts[i][c] += 1
    
    gamma = epsilon = ''
    for counter in counts:
        ranking = counter.most_common()
        gamma += ranking[0][0]
        epsilon += ranking[-1][0]
    return bin_to_dec(gamma) * bin_to_dec(epsilon)


def get_rating(lines, rating_type):
    if rating_type == 'oxygen':
        ranking_index = 0
    elif rating_type == 'co2':
        ranking_index = 1
    else:
        raise Exception('rating_type not recognized')

    i = 0
    line_len = len(lines[0])
    while len(lines) > 1:
        counter = Counter()
        
        for line in lines:
            counter[line[i]] += 1

        most_common = counter.most_common()[0]
        least_common = counter.most_common()[-1]

        if least_common[1] == most_common[1] and least_common[0] != most_common[0]:
            remainer = str(1 - ranking_index)
            print(least_common, most_common)
        else:
            remainer = most_common = counter.most_common()[ranking_index][0]

        new_lines = [line for line in lines if line[i] == remainer]

        lines = new_lines
        i += 1
        i = i % line_len

    return bin_to_dec(lines[0])


def part_2(lines):

    oxygen = get_rating(lines, 'oxygen')
    co2 = get_rating(lines, 'co2')

    return oxygen * co2
    


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, prompt='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(3, example=example)))


if __name__ == '__main__':
    main()