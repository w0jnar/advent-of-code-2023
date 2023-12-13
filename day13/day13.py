def calc_mirror_lists(mirror_file_name, is_part_2=False):
    map_list = []
    with open(mirror_file_name) as f:
        for line in f:
            map_list.append(line[:-1])
    allowed_smudges = 0 if not is_part_2 else 1
    index = 0
    total = 0
    while index < len(map_list):
        count, index = process_block(
            map_list, index, allowed_smudges)
        total += count
        index += 1
    return total


def process_block(map_list, index, allowed_smudges=0):
    # Process a block of the input, getting the counts for horizontal and vertical.
    temp_list = []
    while index < len(map_list) and map_list[index] != '':
        temp_list.append(map_list[index])
        index += 1
    count_horizontal = process_horizontal(temp_list, allowed_smudges)
    count_vertical = process_vertical(temp_list, allowed_smudges)
    count = count_horizontal * 100 + count_vertical
    return count, index


def process_horizontal(map_sub_list, allowed_smudges):
    # Returns the sum of all horizontal symmetries.
    total = 0
    for r in range(len(map_sub_list) - 1):
        check = range(min(r+1, len(map_sub_list) - 1 - r))
        if all(compare_lists(map_sub_list[r-i], map_sub_list[r+i+1], allowed_smudges) for i in check):
            total += r + 1
    return total


def process_vertical(map_sub_list, allowed_smudges):
    # Transposes list to process it vertically.
    return process_horizontal(list(zip(*map_sub_list[::-1])), allowed_smudges)


def compare_lists(char1, char2, allowed_smudges):
    # Compares two input lists, with an input of allowed_smudges for part 2.
    return sum(a != b for (a, b) in zip(char1, char2)) <= allowed_smudges


if __name__ == "__main__":
    total_example_p1 = calc_mirror_lists('day13\\input_example.txt')
    print(f'Part 1: {total_example_p1}')

    total_example_p2 = calc_mirror_lists(
        'day13\\input_example.txt', True) - total_example_p1
    print(f'Part 2: {total_example_p2}')

    total_input_p1 = calc_mirror_lists('day13\\input.txt')
    print(f'Part 1: {total_input_p1}')

    total_input_p2 = calc_mirror_lists(
        'day13\\input.txt', True) - total_input_p1
    print(f'Part 2: {total_input_p2}')
