import click

from utils.input_parser import parse_lines


def str_to_int_list(input_str):
    return list(map(int, input_str[0].split(',')))


def get_fishes(lines, days):
    fishes = [0] * 9
    for fish in str_to_int_list(lines):
        fishes[fish] += 1

    for d in range(days):
        new_fishes = fishes[1:] + [fishes[0]]
        new_fishes[6] += fishes[0]

        fishes = new_fishes

    return sum(fishes)


def part_1(lines):
    return get_fishes(lines, 80)
    


def part_2(lines):
    return get_fishes(lines, 256)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, prompt='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(6, example=example))) # Replace with day


if __name__ == '__main__':
    main()
