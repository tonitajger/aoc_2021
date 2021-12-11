import click
from collections import Counter

from utils.input_parser import parse_lines




SCORE_DICT = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

INCOMPLETE_SCORE_DICT = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


CLOSE_TO_OPEN = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<' 
}

OPEN_TO_CLOSE = {v: k for k, v in CLOSE_TO_OPEN.items()}

def part_1(lines):

    fails = []
    for i, l in enumerate(lines):
        open_stack = []
        for j, c in enumerate(l):
            if c in CLOSE_TO_OPEN:
                expected_open = CLOSE_TO_OPEN[c]
                previous_open = open_stack.pop()
                if expected_open != previous_open:
                    fails.append(SCORE_DICT[c])
                    break
            else:
                open_stack.append(c)
        
    return sum(fails)


def part_2(lines):
    scores = []
    for i, l in enumerate(lines):
        open_stack = []
        has_failed = False
        for j, c in enumerate(l):
            if c in CLOSE_TO_OPEN:
                expected_open = CLOSE_TO_OPEN[c]
                previous_open = open_stack.pop()
                if expected_open != previous_open:
                    has_failed = True
                    break
            else:
                open_stack.append(c)

        if not has_failed:
            # print(open_stack)
            # print(reversed(open_stack))
            # print()
            score = 0
            close = []
            for c in reversed(open_stack):
                score *= 5
                score += INCOMPLETE_SCORE_DICT[OPEN_TO_CLOSE[c]]
                close.append(OPEN_TO_CLOSE[c])
            scores.append(score)
            print(''.join(close))
    
    sorted_scores = sorted(scores)
    return sorted_scores[int(len(sorted_scores) / 2)]


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(10, example=example))) # Replace with day


if __name__ == '__main__':
    main()