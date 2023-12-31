def evaluate_games(red_cubes, green_cubes, blue_cubes, game_file_name):
    total = 0
    with open(game_file_name) as f:
        for line in f:
            parsed_line_list = parse_game_line(line)
            i = 1
            while i < len(parsed_line_list):
                if (parsed_line_list[i]['red'] <= red_cubes and
                    parsed_line_list[i]['green'] <= green_cubes and
                        parsed_line_list[i]['blue'] <= blue_cubes):
                    i += 1
                    if i == len(parsed_line_list):
                        total += parsed_line_list[0]
                else:
                    break
    return total


def evaluate_games_power(game_file_name):
    total = 0
    with open(game_file_name) as f:
        for line in f:
            parsed_line_list = parse_game_line(line)
            minimum_red_cubes = 0
            minimum_green_cubes = 0
            minimum_blue_cubes = 0
            i = 1
            while i < len(parsed_line_list):
                if minimum_red_cubes < parsed_line_list[i]['red']:
                    minimum_red_cubes = parsed_line_list[i]['red']
                if minimum_green_cubes < parsed_line_list[i]['green']:
                    minimum_green_cubes = parsed_line_list[i]['green']
                if minimum_blue_cubes < parsed_line_list[i]['blue']:
                    minimum_blue_cubes = parsed_line_list[i]['blue']
                i += 1
            total += (minimum_red_cubes *
                      minimum_green_cubes * minimum_blue_cubes)
    return total


def parse_game_line(line):
    # Returns list as [game number] followed by the row's games as dictionaries of red/green/blue.
    temp_line_list = line[0:-1].split(':')
    # Get the game number as the first element of the output list.
    output_list = [int(temp_line_list[0].split()[1])]
    # Build the dictionaries of colors.
    for game in temp_line_list[1].split(';'):
        temp_list = game.split(',')
        cube_dict = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for color in temp_list:
            color_list = color[1:].split()
            cube_dict[color_list[1]] = int(color_list[0])
        output_list.append(cube_dict)
    return output_list


if __name__ == "__main__":
    red_cubes = 12
    green_cubes = 13
    blue_cubes = 14
    total = evaluate_games(red_cubes, green_cubes,
                           blue_cubes, 'day02\\input_example.txt')
    print(total)

    total = evaluate_games(red_cubes, green_cubes,
                           blue_cubes, 'day02\\input.txt')
    print(total)

    total = evaluate_games_power('day02\\input_example.txt')
    print(total)

    total = evaluate_games_power('day02\\input.txt')
    print(total)
