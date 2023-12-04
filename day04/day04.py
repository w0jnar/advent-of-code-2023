import pathlib

def check_scratchcards_for_score(scratchcard_file_name):
    total = 0
    with pathlib.Path(scratchcard_file_name).absolute().open() as f:
        for line in f:
            total += process_scratchcard_for_score(line)
    return total

def process_scratchcard_for_score(line):
    score = 0
    winning_numbers, our_numbers = get_number_lists(line)
    for number in winning_numbers:
        if number in our_numbers:
            if score == 0:
                score = 1
            else:
                score *= 2
    return score

def check_scratchcards_for_copies(scratchcard_file_name):
    total = 0
    file_list = []
    copies_dict = {}
    with pathlib.Path(scratchcard_file_name).absolute().open() as f:
        for line in f:
            file_list.append(line)
    i = 0
    while i < len(file_list):
        # Add one copy for the line we are about to process.
        current_line_key = str(i + 1)
        if current_line_key in copies_dict:
            copies_dict[current_line_key] += 1
        else:
            copies_dict[current_line_key] = 1
        wins = process_scratchcard_for_copies(file_list[i])
        # The max needs to be less than the length of the file, otherwise, we'll go off the scratchcard.
        max = wins if i + 1 + wins < len(file_list) else len(file_list) - i - 1
        j = i + 1
        # Update the dictionary by going key by key for each index after our current by the number of wins, multiplying by our number of copies for the current card.
        while j < i + max + 1:
            copies_to_increase_key = str(j + 1)
            if copies_to_increase_key in copies_dict:
                copies_dict[copies_to_increase_key] += 1 * copies_dict.get(current_line_key)
            else:
                copies_dict[copies_to_increase_key] = 1 * copies_dict.get(current_line_key)
            j += 1
        # 1 for the line being process, and wins for each additional card that comes out of wins.
        total += 1 + max * copies_dict.get(current_line_key)
        i += 1
    return total

def process_scratchcard_for_copies(line):
    wins = 0
    winning_numbers, our_numbers = get_number_lists(line)
    for number in winning_numbers:
        if number in our_numbers:
            wins += 1
    return wins

def get_number_lists(line):
    # Remove the Game number as well as the new line on the end.
    temp_card_string = line[line.find(':')+1:-1]
    temp_list = temp_card_string.split('|')
    winning_numbers = [int(x) for x in temp_list[0].split(' ') if x]
    our_numbers = [int(x) for x in temp_list[1].split(' ') if x]
    return winning_numbers, our_numbers

if __name__ == "__main__":
    total = check_scratchcards_for_score('day04\\input_example.txt')
    print(total)

    total = check_scratchcards_for_score('day04\\input.txt')
    print(total)

    total = check_scratchcards_for_copies('day04\\input_example.txt')
    print(total)

    total = check_scratchcards_for_copies('day04\\input.txt')
    print(total)