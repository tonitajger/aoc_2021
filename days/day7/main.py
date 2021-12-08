import click

from utils.input_parser import parse_list


def get_linear_fuel(submarines, i):
    return sum([abs(el - i) for el in submarines])


def get_arithmetic_fuel(submarines, i):
    total = 0
    for el in submarines:
        diff = abs(el - i) 
        total += int(diff * (diff + 1) / 2)
    return total


def total_fuel(submarines, fuel_calculation):
    min_val = None
    for i in range(min(submarines), max(submarines) + 1):
        total_fuel = fuel_calculation(submarines, i)

        if min_val is None or total_fuel < min_val:
            min_val = total_fuel
    
    return min_val


def part_1(lines):
    return total_fuel(lines, get_linear_fuel)
    

def part_2(lines):
    return total_fuel(lines, get_arithmetic_fuel)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
def main(part):
    print(globals()['part_' + part](parse_list(7, example=False))) # Replace with day


if __name__ == '__main__':
    main()