import pathlib
from functools import reduce


def extrapolate_lines(sensor_file_name, is_reverse=False):
    output_list = []
    with pathlib.Path(sensor_file_name).absolute().open() as f:
        for line in f:
            output_list.append(calc_next(line, is_reverse))
    return reduce((lambda x, y: x + y), output_list)


def calc_next(line, is_reverse):
    line_list = [int(x) for x in line.split()]
    if is_reverse:
        line_list.reverse()
    list_of_lists = [line_list]
    i = 0
    # Build the successive lists until we get a list of all 0s.
    while list_of_lists[i].count(0) != len(list_of_lists[i]):
        next_list = []
        j = 1
        while j < len(list_of_lists[i]):
            next_list.append(list_of_lists[i][j] - list_of_lists[i][j-1])
            j += 1
        list_of_lists.append(next_list)
        i += 1
    # Append a 0 to the list of zeros for calculations.
    list_of_lists[i].append(0)
    # Extrapolate, climbing back up the list of lists, skipping the 0 list.
    i = len(list_of_lists) - 2
    while i >= 0:
        list_of_lists[i].append(
            list_of_lists[i][-1] + list_of_lists[i+1][-1])
        i -= 1
    return list_of_lists[0][-1]


if __name__ == "__main__":
    sum = extrapolate_lines('day09\\input_example.txt')
    print(sum)

    sum = extrapolate_lines('day09\\input.txt')
    print(sum)

    sum = extrapolate_lines('day09\\input_example.txt', True)
    print(sum)

    sum = extrapolate_lines('day09\\input.txt', True)
    print(sum)
