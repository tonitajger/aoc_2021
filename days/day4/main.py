import click

from parse import parse_bingo


def part_1(draw_numbers, boards):
    for n in draw_numbers:
        for b in boards:
            b.draw(n)
            if b.has_bingo():
                return b.get_sum_unmarked() * n
            


def part_2(draw_numbers, boards):
    for n in draw_numbers:
        for i, b in enumerate(boards):
            b.draw(n)
            if b.has_bingo():
                if len(boards) == 1:
                   return b.get_sum_unmarked() * n 
                b.has_won = True
        
        boards = [b for b in boards if not b.has_won]


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
def main(part):
    print(globals()['part_' + part](*parse_bingo(example=False))) # Replace with day


if __name__ == '__main__':
    main()