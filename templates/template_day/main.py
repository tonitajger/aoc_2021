import click

from utils.input_parser import parse_lines


def part_1(lines):
    return


def part_2(lines):
    return


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
def main(part):
    print(globals()['part_' + part](parse_lines(9999))) # Replace with day


if __name__ == '__main__':
    main()