import pathlib

def total_value_from_file(file_name, parse_digits_out_of_strings = False):
    total = 0
    with pathlib.Path(file_name).absolute().open() as f:
        for line in f:
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
    temp_number_list = []
    i = 0
    while i < len(line):
        if line[i].isdigit():
            temp_number_list.append(line[i])
        elif line.find('one', i, i + 3) >= 0:
            temp_number_list.append('1')
        elif line.find('two', i, i + 3) >= 0:
            temp_number_list.append('2')
        elif line.find('three', i, i + 5) >= 0:
            temp_number_list.append('3')
        elif line.find('four', i, i + 4) >= 0:
            temp_number_list.append('4')
        elif line.find('five', i, i + 4) >= 0:
            temp_number_list.append('5')
        elif line.find('six', i, i + 3) >= 0:
            temp_number_list.append('6')
        elif line.find('seven', i, i + 5) >= 0:
            temp_number_list.append('7')
        elif line.find('eight', i, i + 5) >= 0:
            temp_number_list.append('8')
        elif line.find('nine', i, i + 4) >= 0:
            temp_number_list.append('9')
        i += 1
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
