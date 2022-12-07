import click

from utils.input_parser import parse_lines


def parse_target(lines):
    coor_str = lines[0].split(': ')[1].split(', ')

    return [tuple(map(int, c.split('=')[1].split('..'))) for c in coor_str]


def part_1(target):
    (x_min, x_max), (y_min, y_max) = target
    valids = set()
    for vx in range(1, x_max):

        is_valid = False
        has_changed = True
        x = 0
        t = 0
        while (not is_valid) and has_changed:
            new_x = max(vx - t, 0) + x
            has_changed = new_x != x
            is_valid = x_min <= new_x <= x_max
            # print(vx, x, new_x, t, has_changed, is_valid)
            x = new_x
            t += 1
        
        if not is_valid:
            continue
        
        for vy in range(1, 200):

            is_valid = False
            has_changed = True
            y = 0
            t = 0
            while (not is_valid) and y >= y_min:

                new_y = vy - t + y
                is_valid = y_min <= new_y <= y_max
                # print(vy, y, new_y, t, is_valid)
                y = new_y
                t += 1

            
            if not is_valid:
                continue
            
            valids.add((vx, vy))
    
    best_vy = sorted(valids, key=lambda x: x[1], reverse=True)[0][1]
    print(best_vy)
    max_h = sum([i for i in range(best_vy + 1)])
    return max_h


def part_2(target):
    (x_min, x_max), (y_min, y_max) = target
    valids = set()
    for vx in range(1, x_max + 1):
        for vy in range(-500, 500):

            is_valid = False

            x, y = 0, 0
            t = 0
            while (not is_valid) and y >= y_min:

                new_x = max(vx - t, 0) + x
                new_y = vy - t + y
                is_valid = (y_min <= new_y <= y_max) and (x_min <= new_x <= x_max)
                x = new_x
                y = new_y
                t += 1

            
            if is_valid:
                valids.add((vx, vy))
        
    
    # with open('input_files/examples/day17_part_2_answer') as f:
    #     lines = f.read().splitlines()
    # all_pairs = set()
    # for l in lines:
    #     for pair in l.split():
    #         all_pairs.add(tuple(map(int, pair.split(','))))
    
    # print(all_pairs - valids)
    
    return len(valids)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_target(parse_lines(17, example=example)))) # Replace with day


if __name__ == '__main__':
    main()