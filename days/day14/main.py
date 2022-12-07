import click
import copy
from collections import Counter


def parse_manual(day, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        input_str = f.read()

    template, rules_str = input_str.split('\n\n')

    rules = rules_str.splitlines()
    rules = {r.split(' -> ')[0]: r.split(' -> ')[1] for r in rules}
    
    return template, rules


def insert_chars(template, rules):
    new = list(template)
    for i in range(len(template) - 1):
        pair = template[i] + template[i + 1]
        if pair in rules:
            new[i] += rules[pair]

    return ''.join(new)


def part_1(template, rules):
    for i in range(10):
        template = insert_chars(template, rules)
    cnt = Counter(template)
    most_common = cnt.most_common()
    print(most_common[0], most_common[-1])
    return most_common[0][1] - most_common[-1][1]


def pairs_from_template(template):
    pairs = Counter()
    for i in range(len(template) - 1):
        pair = template[i] + template[i + 1]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1

    return pairs
            

def insert_pairs(pairs, rules):
    new = copy.deepcopy(pairs)

    for p, c in pairs.items():
        new_char = rules[p]
        new_pairs = p[0] + new_char, new_char + p[1]
        # print(new_pairs)
        for np in new_pairs:
            if np in new:
                new[np] += c
            else:
                new[np] = c
        new[p] -= c
    return new



def part_2(template, rules):
    pairs = pairs_from_template(template)
    for i in range(40):
        pairs = insert_pairs(pairs, rules)
        # print(i, pairs)
    cnt = Counter()
    for p, c in pairs.items():
        for char in p:
            cnt[char] += c
    for char, c in cnt.items():
        if c % 2 == 0:
            cnt[char] = int(c / 2)
        else:
            cnt[char] = int((c - 1) / 2 + 1)
    most_common = cnt.most_common()
    # print(most_common)
    return most_common[0][1] - most_common[-1][1]


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](*parse_manual(14, example=example))) # Replace with day


if __name__ == '__main__':
    main()