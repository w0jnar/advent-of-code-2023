import copy


def build_file_map(file_name: str) -> list[list[str]]:
    file_map = []
    with open(file_name) as f:
        for line in f:
            file_map.append(list(line[:-1]))
    return file_map


def shift_map_north(file_map: list[list[str]]) -> list[list[str]]:
    new_map = copy.deepcopy(file_map)
    for column in range(len(new_map[0])):
        index = 0
        while index < len(new_map):
            if (
                new_map[index][column] == "O"
                and index > 0
                and new_map[index - 1][column] == "."
            ):
                new_map[index - 1][column] = "O"
                new_map[index][column] = "."
                index -= 1
            else:
                index += 1
    return new_map


def shift_map_south(file_map: list[list[str]]) -> list[list[str]]:
    new_map = copy.deepcopy(file_map)
    for column in range(len(new_map[0])):
        index = len(new_map) - 1
        while index >= 0:
            if (
                new_map[index][column] == "O"
                and index < len(new_map) - 1
                and new_map[index + 1][column] == "."
            ):
                new_map[index + 1][column] = "O"
                new_map[index][column] = "."
                index += 1
            else:
                index -= 1
    return new_map


def shift_map_west(file_map: list[list[str]]) -> list[list[str]]:
    new_map = copy.deepcopy(file_map)
    for line in new_map:
        index = 0
        while index < len(line):
            if line[index] == "O" and index > 0 and line[index - 1] == ".":
                line[index - 1] = "O"
                line[index] = "."
                index -= 1
            else:
                index += 1
    return new_map


def shift_map_east(file_map: list[list[str]]) -> list[list[str]]:
    new_map = copy.deepcopy(file_map)
    for line in new_map:
        index = len(line) - 1
        while index >= 0:
            if line[index] == "O" and index < len(line) - 1 and line[index + 1] == ".":
                line[index + 1] = "O"
                line[index] = "."
                index += 1
            else:
                index -= 1
    return new_map


def calc_load_part1(filename: str) -> int:
    file_map = build_file_map(filename)
    shifted_map = shift_map_north(file_map)
    total = 0
    for index, line in enumerate(shifted_map):
        total += (len(shifted_map) - index) * line.count("O")
        # print(line)
    return total


def calc_load_part2(filename: str, cycles: int = 1) -> int:
    shifted_map = build_file_map(filename)
    seen_states: dict[str, int] = {}
    loads_by_cycle: dict[int, int] = {}
    for cycle_num in range(1, cycles + 1):
        shifted_map = shift_map_north(shifted_map)
        shifted_map = shift_map_west(shifted_map)
        shifted_map = shift_map_south(shifted_map)
        shifted_map = shift_map_east(shifted_map)
        key = "".join("".join(line) for line in shifted_map)
        if key not in seen_states:
            seen_states[key] = cycle_num
            total = 0
            for row_num, line in enumerate(shifted_map):
                total += (len(shifted_map) - row_num) * line.count("O")
            loads_by_cycle[cycle_num] = total
        else:
            cycle_start = seen_states[key]
            period = cycle_num - cycle_start
            target_cycle = cycle_start + (cycles - cycle_start) % period
            return loads_by_cycle[target_cycle]
    return -1


if __name__ == "__main__":
    total_example_p1 = calc_load_part1("day14\\input_example.txt")
    print(f"Part 1: {total_example_p1}")

    total_input_p1 = calc_load_part1("day14\\input.txt")
    print(f"Part 1: {total_input_p1}")

    total_example_p2 = calc_load_part2("day14\\input_example.txt", 1000000000)
    print(f"Part 2: {total_example_p2}")

    total_example_p2 = calc_load_part2("day14\\input.txt", 1000000000)
    print(f"Part 2: {total_example_p2}")
