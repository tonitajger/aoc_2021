from coor_pair import CoorPair


def str_coor_to_int_list(str_coor):
    return list(map(int, str_coor.split(',')))


def lines_to_coor_pair(lines):
    pair_list = []
    for line in lines:
        from_coor, to_coor = list(map(str_coor_to_int_list, line.split(' -> ')))
        pair_list.append(CoorPair(from_coor, to_coor))
    return pair_list
