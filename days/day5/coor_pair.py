import numpy as np


def sign(a):
    return (int(a) >= 0) - (int(a) <= 0)


class CoorPair:
    def __init__(self, from_coor, to_coor):
        self.from_coor = np.array(from_coor)
        self.to_coor = np.array(to_coor)
    
    @property
    def is_horizontal_or_vertical(self):
        diff = self.to_coor - self.from_coor
        if diff[0] == 0 or diff[1] == 0:
            return True
        return False
    
    def get_all_coors(self):

        diff = self.to_coor - self.from_coor

        diff_len = max(np.absolute(diff)) # Not really len but w/e
        direction = diff / diff_len # not really direction but w/e

        coors = []
        for i in range(0, diff_len + 1, sign(diff_len)):
            coors.append(tuple(self.from_coor + i * direction))
        return coors

    def __str__(self):
        return f'{self.from_coor} -> {self.to_coor}'
