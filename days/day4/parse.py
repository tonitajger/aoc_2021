from days.day4.board import Board


from board import Board


def parse_bingo(day=4, example=False):
    if example:
        input_path = f'input_files/examples/day{day}'
    else:
        input_path = f'input_files/day{day}'
    with open(input_path, 'r') as f:
        lines = f.read().splitlines()
    numbers = list(map(int, lines[0].split(',')))
    
    boards = []
    board_list = []
    for line in lines[2:]:
        if line == '':
            boards.append(Board(board_list))
            board_list = []
            continue
        board_list.append(list(map(int, line.split())))
    
    if board_list:
        boards.append(Board(board_list))

    return numbers, boards