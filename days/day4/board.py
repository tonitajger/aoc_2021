from typing import List


class Board:
    def __init__(self, input_list) -> None:
        self.board = []
        self.has_won = False
        for i, row in enumerate(input_list):
            self.board.append([])
            for el in row:
                self.board[i].append(Cell(el))
    
    def draw(self, draw_num):
        for row in self.board:
            for el in row:
                el.draw(draw_num)
    
    def has_bingo(self):
        for row in self.board:
            bingo = True
            for el in row:
                if not el.is_drawn:
                    bingo = False
                    continue
            if bingo:
                return True
        
        for i in range(len(self.board[0])):
            bingo = True
            for row in self.board:
                el = row[i]
                if not el.is_drawn:
                    bingo = False
                    continue
            if bingo:
                return True
        return False

    def get_sum_unmarked(self):
        sum_unmarked = 0
        for row in self.board:
            for el in row:
                if not el.is_drawn:
                    sum_unmarked += el.num
        return sum_unmarked

    def __str__(self):
        rows = [' '.join(list(map(str, row))) for row in self.board]
        return '\n'.join(rows)
        



class Cell:
    def __init__(self, num) -> None:
        self.num = num
        self.is_drawn = False
    
    def draw(self, draw_num):
        if not self.is_drawn:
            self.is_drawn = self.num == draw_num
    
    def __str__(self):
        return f'({self.num}, {self.is_drawn})' 
