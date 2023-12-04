import pathlib
import re

def check_engine(engine_file_name, is_gear_ratio = False):
    total = 0
    # Read all the lines into a list for easy current/previous/next manipulation.
    file_list = []
    with pathlib.Path(engine_file_name).absolute().open() as f:
        for line in f:
            file_list.append(line)
    i = 0
    previous_line = None
    while i < len(file_list):
        line = file_list[i]
        next_line = None if i + 1 == len(file_list) else file_list[i+1]
        if not is_gear_ratio:
            total += process_lines_for_engine(line, previous_line, next_line)
        else:
            total += process_lines_for_gear_ratio(line, previous_line, next_line)
        previous_line = line
        i += 1
    return total

def process_lines_for_engine(line, previous_line, next_line):
    total = 0
    i = 0
    # Loop through the line.
    # If we find a digit, figure out how long the number is.
    # Once we find the number, figure out if it is adjacent.
    while i < len(line):
        if line[i].isdigit():
            current_num_string = line[i]
            j = i + 1
            while j < len(line):
                if line[j].isdigit():
                    current_num_string += line[j]
                    j += 1
                else:
                    is_adjacent = False
                    min = i - 1 if i - 1 >= 0 else i
                    max = j + 1 if j + 1 < len(line) else j
                    regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:+=-]')
                    # Character before.
                    # Character after.
                    # Previous line for the length of the number, +-1 for diagonal.
                    # Next line for the length of the number, +-1 for diagonal.
                    if ((i - 1 >= 0 and regex.search(line[i - 1])) or
                        (j + 1 < len(line) and regex.search(line[j])) or
                        (previous_line is not None and regex.search(previous_line[min:max])) or
                        (next_line is not None and regex.search(next_line[min:max]))):
                        is_adjacent = True
                    if is_adjacent:
                        total += int(current_num_string)
                    i += len(current_num_string) + 1
                    break
        else:
            i += 1
    return total

def process_lines_for_gear_ratio(line, previous_line, next_line):
    total = 0
    i = 0
    while i < len(line):
        if line[i] == '*':
            # Find all possible numbers adjacent to the gear.
            gear_adjacent_list = []
            # Before the *.
            if i - 1 > 0 and line[i-1].isdigit():
                current_num_string = line[i-1]
                j = i - 2
                while j > 0 and line[j].isdigit():
                    current_num_string += line[j]
                    j -= 1
                current_num_string = current_num_string[::-1]
                gear_adjacent_list.append(int(current_num_string))
            # After the *.
            if i + 1 < len(line) and line[i+1].isdigit():
                current_num_string = line[i+1]
                j = i + 2
                while j < len(line) and line[j].isdigit():
                    current_num_string += line[j]
                    j += 1
                gear_adjacent_list.append(int(current_num_string))
            # Previous line.
            if previous_line is not None:
                gear_adjacent_list += process_adjacent_lines_for_gear_ratio(previous_line, i)
            # Next line.
            if next_line is not None:
                gear_adjacent_list += process_adjacent_lines_for_gear_ratio(next_line, i)
            if len(gear_adjacent_list) == 2:
                total += gear_adjacent_list[0] * gear_adjacent_list[1]
        i += 1
    return total

# Process the input line (either previous or next), returning a list of 0/1/2 possible adjacent numbers.
def process_adjacent_lines_for_gear_ratio(line, index):
    min = index - 1 if index - 1 >= 0 else index
    max = index + 1 if index + 1 < len(line) else index
    # Check the up to 3 characters adjacent (either above or below) if there are any digits.
    if re.search("\\d", line[min:max+1]):
        # Start building string from the character directly above or below the *.
        current_string = line[index]
        j = max
        # Starting from the diagonal left character, add digits to the string, looping left.
        while j < len(line) and line[j].isdigit():
            current_string += line[j]
            j += 1
        # Reverse the string once all the digits are in current_string.
        current_string = current_string[::-1]
        j = min
        # Starting from the diagonal right character, add digits to the string, looping right.
        while j >= 0 and line[j].isdigit():
            current_string += line[j]
            j -= 1
        # Reverse the string once all the digits are in current_string.
        current_string = current_string[::-1]
        # Replace all non-digits with space.
        # Split the string into a list on space.
        # Remove list elements if blank.
        # Cast the strings to int.
        return [int(x) for x in re.sub("\\D", ' ', current_string).split()]
    else:
        return []

if __name__ == "__main__":
    total = check_engine('day03\\input_example.txt')
    print(total)

    total = check_engine('day03\\input.txt')
    print(total)

    total = check_engine('day03\\input_example.txt', True)
    print(total)

    total = check_engine('day03\\input.txt', True)
    print(total)
