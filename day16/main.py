import sys

sys.setrecursionlimit(100000)

file_map: list[list[str]] = []
heat_dict: dict[str, int] = {}
position_dict: dict[str, int] = {}


def build_file_map(file_name: str) -> list[list[str]]:
    file_map = []
    with open(file_name) as f:
        for line in f:
            file_map.append(list(line[:-1]))
    return file_map


def traverse(x: int, y: int, direction: str):
    global file_map
    global heat_dict
    global position_dict

    map_direction_key = f"{x}_{y}_{direction}"

    if map_direction_key in position_dict:
        return
    else:
        position_dict[map_direction_key] = 1

    if direction == "r":
        next_coord_pair = (x + 1, y)
    elif direction == "l":
        next_coord_pair = (x - 1, y)
    elif direction == "u":
        next_coord_pair = (x, y - 1)
    elif direction == "d":
        next_coord_pair = (x, y + 1)
    else:
        next_coord_pair = (-1, -1)

    if next_coord_pair[0] < 0 or next_coord_pair[0] > len(file_map[0]) - 1:
        return
    if next_coord_pair[1] < 0 or next_coord_pair[1] > len(file_map) - 1:
        return

    map_key = f"{next_coord_pair[0]}_{next_coord_pair[1]}"
    if map_key in heat_dict:
        heat_dict[map_key] = heat_dict[map_key] + 1
    else:
        heat_dict[map_key] = 1

    # .
    if file_map[next_coord_pair[1]][next_coord_pair[0]] == ".":
        traverse(next_coord_pair[0], next_coord_pair[1], direction)

    # /
    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "/" and direction == "r":
        traverse(next_coord_pair[0], next_coord_pair[1], "u")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "/" and direction == "l":
        traverse(next_coord_pair[0], next_coord_pair[1], "d")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "/" and direction == "u":
        traverse(next_coord_pair[0], next_coord_pair[1], "r")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "/" and direction == "d":
        traverse(next_coord_pair[0], next_coord_pair[1], "l")

    # \
    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "\\" and direction == "r":
        traverse(next_coord_pair[0], next_coord_pair[1], "d")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "\\" and direction == "l":
        traverse(next_coord_pair[0], next_coord_pair[1], "u")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "\\" and direction == "u":
        traverse(next_coord_pair[0], next_coord_pair[1], "l")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "\\" and direction == "d":
        traverse(next_coord_pair[0], next_coord_pair[1], "r")

    # |
    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "|" and direction in (
        "r",
        "l",
    ):
        traverse(next_coord_pair[0], next_coord_pair[1], "u")
        traverse(next_coord_pair[0], next_coord_pair[1], "d")

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "|" and direction in (
        "u",
        "d",
    ):
        traverse(next_coord_pair[0], next_coord_pair[1], direction)

    # -
    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "-" and direction in (
        "r",
        "l",
    ):
        traverse(next_coord_pair[0], next_coord_pair[1], direction)

    elif file_map[next_coord_pair[1]][next_coord_pair[0]] == "-" and direction in (
        "u",
        "d",
    ):
        traverse(next_coord_pair[0], next_coord_pair[1], "r")
        traverse(next_coord_pair[0], next_coord_pair[1], "l")
    return


def calc_part1(file_name: str) -> int:
    global file_map
    file_map = build_file_map(file_name)
    traverse(-1, 0, "r")
    # print(heat_dict.keys())
    # for key in heat_dict.keys():
    #     print(key)
    return len(heat_dict.keys())


def calc_part2(file_name: str) -> int:
    global file_map
    global heat_dict
    global position_dict
    file_map = build_file_map(file_name)
    output_list: list[list[str]] = []

    height = len(file_map)
    width = len(file_map[0])
    # top
    for i in range(0, width):
        heat_dict = {}
        position_dict = {}
        traverse(i, -1, "d")
        output_list.append(list(heat_dict.keys()))
    # bottom
    for i in range(0, width):
        heat_dict = {}
        position_dict = {}
        traverse(i, height, "u")
        output_list.append(list(heat_dict.keys()))
    # left
    for i in range(0, height):
        heat_dict = {}
        position_dict = {}
        traverse(-1, i, "r")
        output_list.append(list(heat_dict.keys()))
    # right
    for i in range(0, height):
        heat_dict = {}
        position_dict = {}
        traverse(width, i, "l")
        output_list.append(list(heat_dict.keys()))
    return max(len(res) for res in output_list)


if __name__ == "__main__":
    total_example_p1 = calc_part1("day16\\input_example.txt")
    print(f"Part 1: {total_example_p1}")

    heat_dict = {}
    position_dict = {}

    total_input_p1 = calc_part1("day16\\input.txt")
    print(f"Part 1: {total_input_p1}")

    heat_dict = {}
    position_dict = {}

    total_example_p2 = calc_part2("day16\\input_example.txt")
    print(f"Part 2: {total_example_p2}")

    heat_dict = {}
    position_dict = {}

    total_input_p2 = calc_part2("day16\\input.txt")
    print(f"Part 2: {total_input_p2}")
