import math
import pathlib


def trace_route(map_file_name):
    map_dictionary = {}
    with pathlib.Path(map_file_name).absolute().open() as f:
        # Convert Ls and Rs to 0s and 1s for later list indexing. Remove end newline.
        route = f.readline().replace('L', '0').replace('R', '1')[:-1]
        # Skip blank line.
        f.readline()
        map_line = f.readline()
        first_key = 'AAA'
        # Skip new line lines.
        while len(map_line) > 1:
            key = map_line[0:3]
            left = map_line[7:10]
            right = map_line[12:15]
            map_dictionary[key] = [left, right]
            map_line = f.readline()
    return process_route(route, first_key, map_dictionary)


def process_route(route, first_key, map_dictionary):
    steps = 0
    index = 0
    current_key = first_key
    while True:
        steps += 1
        current_key = map_dictionary[current_key][int(route[index])]
        if current_key == 'ZZZ':
            return steps
        index += 1
        if index > len(route) - 1:
            index -= len(route)


def trace_multiple_routes(map_file_name):
    map_dictionary = {}
    with pathlib.Path(map_file_name).absolute().open() as f:
        # Convert Ls and Rs to 0s and 1s for later list indexing. Remove end newline.
        route = f.readline().replace('L', '0').replace('R', '1')[:-1]
        # Skip blank line.
        f.readline()
        map_line = f.readline()
        while len(map_line) > 1:
            key = map_line[0:3]
            left = map_line[7:10]
            right = map_line[12:15]
            map_dictionary[key] = [left, right]
            map_line = f.readline()
    key_list = [key for key in list(map_dictionary.keys()) if key[2] == 'A']
    return process_multiple_routes(route, key_list, map_dictionary)


def process_multiple_routes(route, key_list, map_dictionary):
    # Get the lowest step for each key, then return the LCM of those steps.
    # This won't work for all theoretical inputs, but due to the nature of the paths of my input,
    # and likely other AoC inputs assuming similiar generation, this works.
    # This is because each route only has 1 **Z, so each route loop is always the same length and all the route lengths
    # are prime numbers (likely intentional for the puzzle).
    step_list = []
    for key in key_list:
        key_found = False
        steps = 0
        route_index = 0
        current_key = key
        while not key_found:
            steps += 1
            current_key = map_dictionary[current_key][int(route[route_index])]
            if current_key[2] == 'Z':
                step_list.append(steps)
                key_found = True
            route_index += 1
            if route_index > len(route) - 1:
                route_index -= len(route)
    return math.lcm(*step_list)


if __name__ == "__main__":
    output = trace_route('day08\\input_example.txt')
    print(output)

    steps = trace_route('day08\\input.txt')
    print(steps)

    output = trace_multiple_routes('day08\\input_example_two.txt')
    print(output)

    steps = trace_multiple_routes('day08\\input.txt')
    print(steps)
