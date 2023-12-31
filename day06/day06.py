from functools import reduce


def calc_margin_of_errors(races_file_name):
    with open(races_file_name) as f:
        time_list = [int(x) for x in f.readline().split(':')[1].split()]
        distance_list = [int(x) for x in f.readline().split(':')[1].split()]
    margin_list = []
    for i, time in enumerate(time_list):
        margin_list.append(calc_margin_of_error(time, distance_list[i]))
    return reduce((lambda x, y: x * y), margin_list)


def calc_margin_of_errors_no_spaces(races_file_name):
    with open(races_file_name) as f:
        time = int(''.join(filter(str.isdigit, f.readline())))
        distance = int(''.join(filter(str.isdigit, f.readline())))
    return calc_margin_of_error(time, distance)


def calc_margin_of_error(time, distance):
    margin_of_error = 0
    for n in range(time + 1):
        if n * (time - n) > distance:
            margin_of_error += 1
    return margin_of_error


if __name__ == "__main__":
    margin = calc_margin_of_errors('day06\\input_example.txt')
    print(margin)

    margin = calc_margin_of_errors('day06\\input.txt')
    print(margin)

    margin = calc_margin_of_errors_no_spaces('day06\\input_example.txt')
    print(margin)

    margin = calc_margin_of_errors_no_spaces('day06\\input.txt')
    print(margin)
