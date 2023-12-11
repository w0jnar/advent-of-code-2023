from functools import reduce


def check_scratchcards_for_score(scratchcard_file_name):
    total = 0
    with open(scratchcard_file_name) as f:
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
    file_list = []
    with open(scratchcard_file_name) as f:
        for line in f:
            file_list.append(line)
    i = 0
    copies_list = [1] * len(file_list)
    while i < len(file_list):
        wins = process_scratchcard_for_copies(file_list[i])
        # The max needs to be less than the length of the file, otherwise, we'll go off the scratchcard.
        max = wins if i + wins < len(file_list) else len(file_list) - i
        j = i + 1
        # Update the list by going key by key for each index after our current by the number of wins, multiplying by our number of copies for the current card.
        while j < i + max + 1:
            copies_list[j] += 1 * copies_list[i]
            j += 1
        i += 1
    return reduce((lambda x, y: x + y), copies_list)


def process_scratchcard_for_copies(line):
    wins = 0
    winning_numbers, our_numbers = get_number_lists(line)
    for number in winning_numbers:
        if number in our_numbers:
            wins += 1
    return wins


def get_number_lists(line):
    # Remove the Game number and colon, leaving just the numbers.
    temp_card_string = line[line.find(':')+1:]
    temp_list = temp_card_string.split('|')
    winning_numbers = [int(x) for x in temp_list[0].split()]
    our_numbers = [int(x) for x in temp_list[1].split()]
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
