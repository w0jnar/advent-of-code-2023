import pathlib


def total_value_from_file(file_name, parse_digits_out_of_strings=False):
    total = 0
    with pathlib.Path(file_name).absolute().open() as f:
        for line in f:
            # parse_numbers_in_line already returns just the number so no need to filter again.
            if parse_digits_out_of_strings:
                number_string = parse_numbers_in_line(line)
            else:
                number_string = ''.join(filter(str.isdigit, line))
            if len(number_string) == 1:
                total += int(number_string + number_string)
            else:
                total += int(number_string[0] + number_string[-1])
    return total


def parse_numbers_in_line(line):
    # Returns a string of just the numbers, parsing out number words.
    num_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    temp_number_list = []
    for i, character in enumerate(line):
        if character.isdigit():
            temp_number_list.append(character)
        else:
            for key in num_dict:
                if line.find(key, i, i + len(key)) >= 0:
                    temp_number_list.append(num_dict[key])
    return ''.join(temp_number_list)


if __name__ == "__main__":
    total = total_value_from_file('day01\\input_example.txt')
    print(total)

    total = total_value_from_file('day01\\input.txt')
    print(total)

    total = total_value_from_file('day01\\input_example_two.txt', True)
    print(total)

    total = total_value_from_file('day01\\input.txt', True)
    print(total)
