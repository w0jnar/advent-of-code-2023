def check_almanac(almanac_file_name):
    file_list = []
    with open(almanac_file_name) as f:
        for line in f:
            file_list.append(line[:-1])
    # Build dictionaries from file_list.
    (seed_to_soil_dict, soil_to_fertilizer_dict, fertilizer_to_water_dict,
        water_to_light_dict, light_to_temperature_dict, temperature_to_humidity_dict,
        humidity_to_location_dict) = build_almanac_dicts(file_list)
    seed_list = [int(x) for x in file_list[0].split(':')[1].split()]

    def get_location(seed, seed_to_soil_dict, soil_to_fertilizer_dict, fertilizer_to_water_dict,
                     water_to_light_dict, light_to_temperature_dict, temperature_to_humidity_dict,
                     humidity_to_location_dict):
        soil = get_value_from_almanac_dict(seed_to_soil_dict, seed)
        fertilizer = get_value_from_almanac_dict(soil_to_fertilizer_dict, soil)
        water = get_value_from_almanac_dict(
            fertilizer_to_water_dict, fertilizer)
        light = get_value_from_almanac_dict(water_to_light_dict, water)
        temperature = get_value_from_almanac_dict(
            light_to_temperature_dict, light)
        humidity = get_value_from_almanac_dict(
            temperature_to_humidity_dict, temperature)
        return get_value_from_almanac_dict(humidity_to_location_dict, humidity)
    # Wrap min in local function to get lowest locaton for each seed.
    return min([get_location(seed, seed_to_soil_dict, soil_to_fertilizer_dict, fertilizer_to_water_dict,
                             water_to_light_dict, light_to_temperature_dict, temperature_to_humidity_dict,
                             humidity_to_location_dict) for seed in seed_list])


def check_almanac_reverse(almanac_file_name):
    file_list = []
    with open(almanac_file_name) as f:
        for line in f:
            file_list.append(line[:-1])
    # Build dictionaries from file_list.
    (seed_to_soil_dict, soil_to_fertilizer_dict, fertilizer_to_water_dict,
        water_to_light_dict, light_to_temperature_dict, temperature_to_humidity_dict,
        humidity_to_location_dict) = build_almanac_dicts(file_list)
    temp_seed_list = [int(x) for x in file_list[0].split(':')[1].split()]
    i = 0
    seed_range_list = []
    while i < len(temp_seed_list):
        seed_range_list.append(
            range(temp_seed_list[i], (temp_seed_list[i] + temp_seed_list[i+1])))
        i += 2
    # Starting from location 0, brute force through the dictionaries in reverse until there's a matching seed, then return location.
    location = 0
    is_location_found = False
    while not is_location_found:
        humidity = get_key_from_almanac_dict(
            humidity_to_location_dict, location)
        temperature = get_key_from_almanac_dict(
            temperature_to_humidity_dict, humidity)
        light = get_key_from_almanac_dict(
            light_to_temperature_dict, temperature)
        water = get_key_from_almanac_dict(water_to_light_dict, light)
        fertilizer = get_key_from_almanac_dict(fertilizer_to_water_dict, water)
        soil = get_key_from_almanac_dict(soil_to_fertilizer_dict, fertilizer)
        seed = get_key_from_almanac_dict(seed_to_soil_dict, soil)
        for seed_range in seed_range_list:
            if seed in seed_range:
                is_location_found = True
        if not is_location_found:
            location += 1
    return location


def build_almanac_dicts(file_list):
    # Build dictionaries from file, based on name.
    seed_to_soil_dict = {}
    soil_to_fertilizer_dict = {}
    fertilizer_to_water_dict = {}
    water_to_light_dict = {}
    light_to_temperature_dict = {}
    temperature_to_humidity_dict = {}
    humidity_to_location_dict = {}
    line_number = 0
    while line_number < len(file_list):
        if 'map' in file_list[line_number]:
            line_number += build_almanac_dict(file_list, line_number, eval(
                f'{file_list[line_number].split()[0].replace('-', '_')}_dict'))
        line_number += 1
    return (seed_to_soil_dict, soil_to_fertilizer_dict, fertilizer_to_water_dict,
            water_to_light_dict, light_to_temperature_dict, temperature_to_humidity_dict,
            humidity_to_location_dict)


def build_almanac_dict(file_list, index, dictionary):
    # Build the individual dictionaries from the file blocks.
    i = index + 1
    while i < len(file_list) and len(file_list[i]) > 0:
        map_line = [int(x) for x in file_list[i].split()]
        destination_range = map_line[0]
        source_range = map_line[1]
        range_length = map_line[2]
        source_range_end = source_range + range_length - 1
        destination_range_end = destination_range + range_length - 1
        dictionary[f'{source_range},{source_range_end}'] = f'{
            destination_range},{destination_range_end}'
        i += 1
    return i - index


def get_value_from_almanac_dict(dictionary, input_value):
    # Dictionary lookup to get the specific individual value from the map based on the key/value ranges.
    output = input_value
    for key in dictionary:
        key_range_list = [int(x) for x in key.split(',')]
        key_lower_range = key_range_list[0]
        key_upper_range = key_range_list[1]
        if input_value >= key_lower_range and input_value <= key_upper_range:
            value_range_lower = int(dictionary[key].split(',')[0])
            offset = value_range_lower - key_lower_range
            output = offset + input_value
            break
    return output


def get_key_from_almanac_dict(dictionary, input_value):
    # Dictionary lookup to get the specific individual key from the map based on the key/value ranges.
    # Essentially reverse of get_value_from_almanac_dict, getting the key instead of the value.
    output = input_value
    for key in dictionary:
        value_range_list = [int(x) for x in dictionary[key].split(',')]
        value_lower_range = value_range_list[0]
        value_upper_range = value_range_list[1]
        if input_value >= value_lower_range and input_value <= value_upper_range:
            key_range_lower = int(key.split(',')[0])
            offset = key_range_lower - value_lower_range
            output = offset + input_value
            break
    return output


if __name__ == "__main__":
    location = check_almanac('day05\\input_example.txt')
    print(location)

    location = check_almanac('day05\\input.txt')
    print(location)

    location = check_almanac_reverse('day05\\input_example.txt')
    print(location)

    location = check_almanac_reverse('day05\\input.txt')
    print(location)
