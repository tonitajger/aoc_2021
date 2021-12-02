import click

from utils.input_parser import parse_lines


def part_1(lines):
    x = d = 0
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)
        if direction == 'forward':
            x += amount
        elif direction == 'up':
            d -= amount
        elif direction == 'down':
            d += amount
    return x * d


def part_2(lines):
    x = d = a = 0
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)
        if direction == 'forward':
            x += amount
            d += a * amount
        elif direction == 'up':
            a -= amount
        elif direction == 'down':
            a += amount
    return x * d


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
def main(part):
    print(globals()['part_' + part](parse_lines(2)))


if __name__ == '__main__':
    main()