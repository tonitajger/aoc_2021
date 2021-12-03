def parse_lines(day, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        lines = f.read().splitlines()
    return lines
