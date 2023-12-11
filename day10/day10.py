def map_distance(map_file_name):
    pipe_map = PipeMap(map_file_name)
    pipe_map.generate_map_list()
    furthest = pipe_map.find_furthest()
    print(f'Furthest: {furthest}')
    area = pipe_map.find_area()
    print(f'Area: {area}')


class PipeMap:
    def __init__(self, map_file_name):
        self.map_file_name = map_file_name
        self.map_list = []
        self.map_dict = {}
        self.s_x = None
        self.s_y = None
        self.s_char = None

    def generate_map_list(self):
        with open(self.map_file_name) as f:
            for line in f:
                self.map_list.append(line[:-1])

    def find_furthest(self):
        # Gets the two positions off of S and traverses the pipes until both routes hit the same pipe, as that would be the furthest pipe.
        self._find_s()
        s_pos = self._format_dict_string(self.s_y, self.s_x)
        current_1, current_2 = self._find_next_from_s()
        self._find_s_char(current_1, current_2)
        previous_1 = s_pos
        previous_2 = s_pos
        step = 1
        while current_1 != current_2:
            step += 1
            current_1_holder = current_1
            current_1 = self._find_next(current_1, previous_1, step)
            previous_1 = current_1_holder
            current_2_holder = current_2
            current_2 = self._find_next(current_2, previous_2, step)
            previous_2 = current_2_holder
        return step

    def _find_s(self):
        for i, line in enumerate(self.map_list):
            if line.find('S') >= 0:
                self.s_x = line.find('S')
                self.s_y = i
                break
        self.map_dict[self._format_dict_string(self.s_y, self.s_x)] = 0

    def _find_next_from_s(self):
        # Find the 2 positions off of S.
        one_positions = []
        if self.s_x - 1 >= 0 and self.map_list[self.s_y][self.s_x - 1] in ('-', 'L', 'F'):
            current_formatted_string = self._format_dict_string(
                self.s_y, (self.s_x - 1))
            one_positions.append(current_formatted_string)
        if self.s_x + 1 < len(self.map_list[0]) and self.map_list[self.s_y][self.s_x + 1] in ('-', 'J', '7'):
            current_formatted_string = self._format_dict_string(
                self.s_y, (self.s_x + 1))
            one_positions.append(current_formatted_string)
        if self.s_y - 1 >= 0 and self.map_list[self.s_y - 1][self.s_x] in ('|', '7', 'F'):
            current_formatted_string = self._format_dict_string(
                (self.s_y - 1), self.s_x)
            one_positions.append(current_formatted_string)
        if self.s_y + 1 < len(self.map_list) and self.map_list[self.s_y + 1][self.s_x] in ('|', 'L', 'J'):
            current_formatted_string = self._format_dict_string(
                (self.s_y + 1), self.s_x)
            one_positions.append(current_formatted_string)
        for position in one_positions:
            self.map_dict[position] = 1
        return one_positions[0], one_positions[1]

    def _find_next(self, current, previous, step):
        # Find the next position, keeping track of the previous to continue progressing.
        current_list = [int(i) for i in current.split('_')]
        previous_list = [int(i) for i in previous.split('_')]
        current_y = current_list[0]
        current_x = current_list[1]
        previous_y = previous_list[0]
        previous_x = previous_list[1]
        if (current_x - 1 != previous_x and current_x - 1 >= 0 and
                self.map_list[current_y][current_x] in ('-', 'J', '7') and
                self.map_list[current_y][current_x - 1] in ('-', 'L', 'F')):
            next_position = self._format_dict_string(
                current_y, (current_x - 1))
        elif (current_x + 1 != previous_x and current_x + 1 < len(self.map_list[0]) and
                self.map_list[current_y][current_x] in ('-', 'L', 'F') and
                self.map_list[current_y][current_x + 1] in ('-', 'J', '7')):
            next_position = self._format_dict_string(
                current_y, (current_x + 1))
        elif (current_y - 1 != previous_y and current_y - 1 >= 0 and
                self.map_list[current_y][current_x] in ('|', 'L', 'J') and
                self.map_list[current_y - 1][current_x] in ('|', '7', 'F')):
            next_position = self._format_dict_string(
                (current_y - 1), current_x)
        elif (current_y + 1 != previous_y and current_y + 1 < len(self.map_list) and
                self.map_list[current_y][current_x] in ('|', '7', 'F') and
                self.map_list[current_y + 1][current_x] in ('|', 'L', 'J')):
            next_position = self._format_dict_string(
                (current_y + 1), current_x)
        self.map_dict[next_position] = step
        return next_position

    def _format_dict_string(self, y, x):
        return f'{y}_{x}'

    def _find(self, position):
        # Find in self.map_list with self.map_dict string format.
        position_list = [int(i) for i in position.split('_')]
        return self.map_list[position_list[0]][position_list[1]]

    def find_area(self):
        # Loop through the list, toggling between inside and and not inside based on when we are next to an opening or closing edge pipe.
        # Copy the map to leave S in place.
        map_copy = self.map_list.copy()
        temp_string = map_copy[self.s_y].replace('S', self.s_char)
        map_copy[self.s_y] = temp_string
        area = 0
        for i, line in enumerate(map_copy):
            inside = False
            for j, _ in enumerate(line):
                if self.map_dict.get(self._format_dict_string(i, j), None) is not None:
                    if map_copy[i][j] in ('|', 'J', 'L'):
                        inside = not inside
                else:
                    area += inside
        return area

    def _find_s_char(self, current_1, current_2):
        # Figure out which character should be in S position for area.
        # Find the 4 coordinates around S, then figure out where the 2 coords are in regard to S,
        # aka, North/South/East/West of S.
        north_coord = self._format_dict_string((self.s_y - 1), self.s_x)
        south_coord = self._format_dict_string((self.s_y + 1), self.s_x)
        west_coord = self._format_dict_string(self.s_y, (self.s_x - 1))
        east_coord = self._format_dict_string(self.s_y, (self.s_x + 1))
        is_north = False
        is_south = False
        is_west = False
        is_east = False
        if north_coord in (current_1, current_2):
            is_north = True
        if south_coord in (current_1, current_2):
            is_south = True
        if west_coord in (current_1, current_2):
            is_west = True
        if east_coord in (current_1, current_2):
            is_east = True
        if is_north and is_south:
            self.s_char = '|'
        elif is_east and is_west:
            self.s_char = '-'
        elif is_north and is_east:
            self.s_char = 'L'
        elif is_north and is_west:
            self.s_char = 'J'
        elif is_south and is_west:
            self.s_char = '7'
        elif is_south and is_east:
            self.s_char = 'F'


if __name__ == "__main__":
    map_distance('day10\\input_example.txt')

    map_distance('day10\\input.txt')

    map_distance('day10\\input_example_two.txt')
