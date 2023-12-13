from functools import cache


def find_possible_spring_record(spring_record_file_name, is_part_2=False):
    total = 0
    copies = 1 if not is_part_2 else 5
    with open(spring_record_file_name) as f:
        for line in f:
            total += find_possible_arrangements(line, copies)
    return total


def find_possible_arrangements(line, copies=1):
    line_portions = line.split()
    string_to_check = tuple((line_portions[0] + '?') * copies)
    match_tuple = tuple(int(x) for x in line_portions[1].split(',')) * copies
    return evaluate_string(string_to_check, match_tuple, 0, 0)


@cache
def evaluate_string(string_to_check, match_tuple, index, match_index, total=0):
    if index == len(string_to_check):
        return match_index == len(match_tuple)
    if string_to_check[index] in ('.', '?'):
        total += evaluate_string(string_to_check,
                                 match_tuple, index+1, match_index)
    try:
        offset = index + match_tuple[match_index]
        if string_to_check[index] in ('#', '?') and '.' not in string_to_check[index:offset] and '#' not in string_to_check[offset]:
            total += evaluate_string(string_to_check,
                                     match_tuple, offset+1, match_index+1)
    except IndexError:
        pass
    return total


if __name__ == "__main__":
    total = find_possible_spring_record('day12\\input_example.txt')
    print(f'Part 1: {total}')

    total = find_possible_spring_record('day12\\input.txt')
    print(f'Part 1: {total}')

    total = find_possible_spring_record('day12\\input_example.txt', True)
    print(f'Part 2: {total}')

    total = find_possible_spring_record('day12\\input.txt', True)
    print(f'Part 2: {total}')
