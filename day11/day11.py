def map_distance(galaxy_map_file_name):
    galaxy_map = GalaxyMap(galaxy_map_file_name)
    galaxy_map.generate_galaxy_list()
    print(f'Part 1: {galaxy_map.calc_distances()}')
    print(f'Part 2: {galaxy_map.calc_distances(True)}')


class GalaxyMap:
    def __init__(self, galaxy_map_file_name):
        self.galaxy_map_file_name = galaxy_map_file_name
        self.galaxies = []
        self.expand_x = []
        self.expand_y = []

    def generate_galaxy_list(self):
        # Generates the list of galaxies as XY coords, as well as the indices of the expanses.
        map_list = []
        with open(self.galaxy_map_file_name) as f:
            for line in f:
                map_list.append(line[:-1])
                if line[:-1].count('.') == len(line) - 1:
                    self.expand_y.append(len(map_list) - 1)
        i = 0
        while i < len(map_list[0]):
            for j, line in enumerate(map_list):
                if line[i] == '#':
                    break
                if j == len(map_list) - 1:
                    self.expand_x.append(i)
            i += 1
        self.galaxies = [(x, y) for x, line in enumerate(map_list)
                         for y, col in enumerate(line) if col == "#"]

    def calc_distances(self, is_part_2=False):
        # Iterate through the list of galaxies, comparing each pair,
        # increasing the distance if we hit an expanse based on part 1 or 2.
        distance = 0
        for i in range(len(self.galaxies) - 1):
            for j in range(i + 1, len(self.galaxies)):
                (x1, y1), (x2, y2) = self.galaxies[i], self.galaxies[j]
                for num in self.expand_y:
                    if x1 < num < x2 or x2 < num < x1:
                        distance += 1 if not is_part_2 else 999999
                for num in self.expand_x:
                    if y1 < num < y2 or y2 < num < y1:
                        distance += 1 if not is_part_2 else 999999
                distance += abs(x1 - x2) + abs(y2 - y1)
        return distance


if __name__ == "__main__":
    map_distance('day11\\input_example.txt')

    map_distance('day11\\input.txt')
