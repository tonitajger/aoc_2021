import click

from utils.input_parser import parse_lines


def part_1(input_lines):
    increases = 0
    for i in range(1, len(input_lines)):
        if int(input_lines[i]) > int(input_lines[i-1]):
            increases += 1
    return increases


def part_2(input_lines):
    increases = 0
    for i in range(4, len(input_lines)+1):
        if sum(map(int, input_lines[i-4:i-1])) < sum(map(int, input_lines[i-3:i])):
            increases += 1
    return increases


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, prompt='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(1, example=example)))


if __name__ == '__main__':
    main()