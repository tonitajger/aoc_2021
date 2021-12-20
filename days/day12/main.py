import click
import copy

from utils.input_parser import parse_lines


class Node:
    def __init__(self, name, adj = None) -> None:
        self.name = name
        self.is_lower = name.lower() == name
        if adj is None:
            self.adj = []
        else:
            self.adj = adj
        self.parent = None
        self.visited = False
    
    def connect(self, other_node):
        self.adj.append(other_node)
        other_node.adj.append(self)


def parse_edges(lines):
    graph = {}
    for l in lines:
        from_node_name, to_node_name = l.split('-')
        if from_node_name in graph:
            from_node = graph[from_node_name]
        else:
            from_node = Node(from_node_name)
            graph[from_node_name] = from_node
        if to_node_name in graph:
            to_node = graph[to_node_name]
        else:
            to_node = Node(to_node_name)
            graph[to_node_name] = to_node

        from_node.connect(to_node)
        
    return graph


def sum_paths_start(graph):
    visited = set()
    return sum_paths(graph['start'], visited)


def sum_paths(node, visited):
    if node.name == 'end':
        return 1
    
    if node.name == node.name.lower():
        visited.add(node.name)
    return sum([sum_paths(a, copy.deepcopy(visited)) for a in node.adj if a.name not in visited])


def sum_paths_start_2(graph):
    visited = set()
    return sum_paths_2(graph['start'], visited, False)


def sum_paths_2(node, visited, twiced):
    if node.name == 'end':
        return 1
    
    if node.name == node.name.lower():
        visited.add(node.name)

    sub_sum = 0
    for a in node.adj:
        if a.name not in visited:
            sub_sum += sum_paths_2(a, copy.deepcopy(visited), twiced)
        elif not twiced and a.name not in {'start', 'end'}:
            sub_sum += sum_paths_2(a, copy.deepcopy(visited), True)
    return sub_sum


def part_1(lines):
    graph = parse_edges(lines)
    return sum_paths_start(graph)


def part_2(lines):
    graph = parse_edges(lines)
    return sum_paths_start_2(graph)


@click.command()
@click.option('--part', '-p', prompt='Part 1 or 2?')
@click.option('--example', '-e', is_flag=True, help='Run with example?')
def main(part, example):
    print(globals()['part_' + part](parse_lines(12, example=example))) # Replace with day


if __name__ == '__main__':
    main()










