import click
import numpy as np

import tqdm
from utils.input_parser import parse_lines


import matplotlib as plt


def lines_to_instructions(lines):
    instructions = []
    for l in lines:
        onoff_str, coors_str = l.split()
        on = onoff_str == 'on'
        coors = [tuple(map(int, c.split('=')[-1].split('..'))) for c in coors_str.split(',')]
        instructions.append((on, coors))

    return instructions


def create_grid():
    return 


def part_1(lines):
    grid = np.zeros((101, 101, 101), dtype=int)
    for on, coors in lines_to_instructions(lines):
        for c in coors:
            for el in c:
                if abs(el) > 50:
                    continue
        val = 1 if on else 0

        desired_shape = grid[coors[0][0] + 50:coors[0][1] + 1 + 50, coors[1][0] + 50:coors[1][1] + 1 + 50, coors[2][0] + 50:coors[2][1] + 1 + 50].shape
        grid[coors[0][0] + 50:coors[0][1] + 1 + 50, coors[1][0] + 50:coors[1][1] + 1 + 50, coors[2][0] + 50:coors[2][1] + 1 + 50] = np.ones(desired_shape) * val

    return np.sum(grid)



def part_2_depr(lines):
    # return  lines_to_instructions(lines)
    for on, coors in tqdm.tqdm(lines_to_instructions(lines)):

        existing_coors = set()
        if on:
            for i in range(coors[0][0], coors[0][1] + 1):
                for j in range(coors[1][0], coors[1][1] + 1):
                    for k in range(coors[2][0], coors[2][1] + 1):
                        existing_coors.add((i, j, k))
    
    sum_on = 0
    print('summing')
    for c in  tqdm.tqdm(existing_coors):
        for on, coors in lines_to_instructions(lines[::-1]):
            if on:
                x_in_range = coors[0][0] <= c[0] <= coors[0][1]
                if not x_in_range:
                    continue
                y_in_range = coors[1][0] <= c[0] <= coors[1][1]
                if not y_in_range:
                    continue
                z_in_range = coors[2][0] <= c[0] <= coors[2][1]
                if not z_in_range:
                    continue
                sum_on += 1

    return sum_on



class Block:
    def __init__(self, on, coors, overlapped=False, sign=None) -> None:
        self.coors = coors
        self.x = coors[0]
        self.y = coors[1]
        self.z = coors[2]
        self.on = on
        self.sign = sign
        if sign == None:
            if on:
                self.sign = 1
            else:
                self.sign = 0

        self.overlapped = overlapped
    
    @property
    def x_min(self):
        return min(self.x)
    
    @property
    def x_max(self):
        return max(self.x)
    
    @property
    def y_min(self):
        return min(self.y)
    
    @property
    def y_max(self):
        return max(self.y)
    
    @property
    def z_min(self):
        return min(self.z)
    
    @property
    def z_max(self):
        return max(self.z)
    
    @property
    def is_too_large(self):
        for c in self.coors:
            for el in c:
                if abs(el) > 50:
                    return True
        return False

    @property
    def volume(self):
        return (self.x_max + 1 - self.x_min) * (self.y_max + 1 - self.y_min) * (self.z_max + 1 - self.z_min)
    
    def __repr__(self) -> str:
        return f"Block: {self.on}, {self.coors}, {self.sign}"





def overlap(b1, b2):
    if not b1.on and not b2.on:
        return None
    x_min = max(b1.x_min, b2.x_min)
    y_min = max(b1.y_min, b2.y_min)
    z_min = max(b1.z_min, b2.z_min)
    x_max = min(b1.x_max, b2.x_max)
    y_max = min(b1.y_max, b2.y_max)
    z_max = min(b1.z_max, b2.z_max)


    if x_min >= x_max:
        return
    if y_min >= y_max:
        return
    if z_min >= z_max:
        return

    return Block(b1.on, ((x_min, x_max), (y_min, y_max), (z_min, z_max)), overlapped=True, sign=b1.sign * -1 * b2.sign )


def part_2(lines):
    blocks = [Block(on, coors) for on, coors in lines_to_instructions(lines)]
    blocks = [b for b in blocks if not b.is_too_large]

    overlaps = []
    sum = 0
    grid = np.zeros((101, 101, 101), dtype=int)
    for i, b in enumerate(blocks):
        print(b, b.volume)
        on = b.on
        coors = b.coors
        for c in coors:
            for el in c:
                if abs(el) > 50:
                    continue
        val = 1 if on else 0

        desired_shape = grid[coors[0][0] + 50:coors[0][1] + 1 + 50, coors[1][0] + 50:coors[1][1] + 1 + 50, coors[2][0] + 50:coors[2][1] + 1 + 50].shape
        grid[coors[0][0] + 50:coors[0][1] + 1 + 50, coors[1][0] + 50:coors[1][1] + 1 + 50, coors[2][0] + 50:coors[2][1] + 1 + 50] = np.ones(desired_shape) * val
        print("sol1", np.sum(grid))


        overlapped_overlaps = []

        for other_b in overlaps:
            
            o = overlap(b, other_b)
            if o:

                print("overlap1:", o, o.volume)
                overlapped_overlaps.append(o)

        overlaps.extend(overlapped_overlaps)
        overlapped_blocks = []
        
        for other_b in blocks[:i]:
            print(f"other: {other_b}", other_b.volume)
            
            o = overlap(b, other_b)
            if o:
                print("overlap2:", o, o.volume)
                overlapped_blocks.append(o)
                overlaps.append(o)
        
       
            
        if b.on:
            sum += b.volume
        
            for overlap_b in overlapped_blocks:
                if overlap_b.on:
                    sum += overlap_b.volume * overlap_b.sign
            
            for overlap_b in overlapped_overlaps:
                if overlap_b.on:
                    sum += overlap_b.volume * overlap_b.sign
        
        else:
            for overlap_b in overlapped_blocks:
                if not overlap_b.on:
                    sum -= overlap_b.volume
        
        print("sol2", sum, "\n")

    return np.sum(grid)


    sum = 0
    for i, b in enumerate(blocks[:12]):
        print("current:", i, b, b.volume)

        overlapped_overlaps = []

        for other_b in overlaps:
            
            o = overlap(b, other_b)
            if o:

                print("overlap1:", o, o.volume)
                overlapped_overlaps.append(o)

        overlaps.extend(overlapped_overlaps)
        overlapped_blocks = []
        
        for other_b in blocks[:i]:
            print(f"other: {other_b}", other_b.volume)
            
            o = overlap(b, other_b)
            if o:
                print("overlap2:", o, o.volume)
                overlapped_blocks.append(o)
                overlaps.append(o)
        
       
            
        if b.on:
            sum += b.volume
        
            for overlap_b in overlapped_blocks:
                if overlap_b.on:
                    sum += overlap_b.volume * overlap_b.sign
            
            for overlap_b in overlapped_overlaps:
                if overlap_b.on:
                    sum += overlap_b.volume * overlap_b.sign
        
        else:
            for overlap_b in overlapped_blocks:
                if not overlap_b.on:
                    sum -= overlap_b.volume
        
        print(sum)


    return sum
            

                


    print(blocks[0], blocks[1])
    print(overlap(blocks[0], blocks[1]))
    


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(22, example=example))) # Replace with day


if __name__ == '__main__':
    main()