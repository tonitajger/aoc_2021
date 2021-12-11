from matplotlib import cm
import numpy as np
from PIL import Image

from utils.input_parser import parse_lines

from main import parse_grid, flash_grid

frames = []
im_counter = 0
def take_image(im):
    frames.append(Image.fromarray(np.uint8(cm.plasma(im)*255)).resize((128,128), resample=Image.NEAREST))


def get_grid_witout_padding(grid):
    return grid[1:-1, 1:-1]



def part_2(lines):
    grid = np.pad(parse_grid(lines), 1)
    counter = 1
    while True:
        grid += 1
        inner = get_grid_witout_padding(grid)
        
        flash_grid(grid)

        if counter % 5 == 0:
            # take_image((inner >= 9) * inner/9) # only flashes
            take_image(inner/9)

        if np.sum(grid[1:-1, 1:-1]) == 0:
            take_image(inner/9)
            # take_image((inner >= 9) * inner/9) # only flashes
            return counter
        counter += 1


def main():
    part_2(parse_lines(11))
    if frames:
        # Save GIF
        frames[0].save(
            'visualization/day11_octupus_flash.gif', 
            save_all=True,
            append_images=frames[1:], 
            optimize=False, 
            duration=[1] * (len(frames) - 1) + [1000],
            loop=0,
            subsampling=0,
            quality=100
        )

if __name__ == '__main__':
    main()