def hash_algo(piece: str) -> int:
    total = 0
    for char in piece:
        total += ord(char)
        total = total * 17
        total = total % 256
    # print(f"{piece}:{total}")
    return total


def calc_part1(file_name: str) -> int:
    with open(file_name) as f:
        split_string_list = str(f.readline()[:-1]).split(",")
    total = 0
    for piece in split_string_list:
        total += hash_algo(piece)
    return total


def calc_part2(file_name: str) -> int:
    with open(file_name) as f:
        split_string_list = str(f.readline()[:-1]).split(",")
    boxes: list[list[dict[str, int]]] = [[] for _ in range(256)]
    for piece in split_string_list:
        if "=" in piece:
            piece_split = piece.split("=")
            char = piece_split[0]
            focal = int(piece_split[1])
            box_num = hash_algo(char)
            is_new = True
            for lenses in boxes[box_num]:
                if char in lenses:
                    lenses[char] = focal
                    is_new = False
                    break
            if is_new:
                boxes[box_num].append({char: focal})
        else:
            char = piece[:-1]
            box_num = hash_algo(char)
            index = -1
            for i, lenses in enumerate(boxes[box_num]):
                if char in lenses:
                    index = i
                    break
            if index > -1:
                del boxes[box_num][index]
    # print(boxes)
    total = 0
    for x, box in enumerate(boxes):
        for y, slot in enumerate(box):
            total += (1 + x) * (1 + y) * (list(slot.values())[0])
    return total


if __name__ == "__main__":
    total_example_p1 = calc_part1("day15\\input_example.txt")
    print(f"Part 1: {total_example_p1}")

    total_input_p1 = calc_part1("day15\\input.txt")
    print(f"Part 1: {total_input_p1}")

    total_example_p2 = calc_part2("day15\\input_example.txt")
    print(f"Part 2: {total_example_p2}")

    total_input_p2 = calc_part2("day15\\input.txt")
    print(f"Part 2: {total_input_p2}")
