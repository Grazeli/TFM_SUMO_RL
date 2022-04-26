def kmh_to_ms(speed_kmh: float):
    """
    This function is used to convert a speed value from km/h to m/s

    :param float speed_kmh: Km/s speed to be converted to m/s
    :return float: Return the given speed in m/s 
    """
    return speed_kmh / 3.6


def write_in_txt(filepath: str, param_list: list):
    """
    This function is to write a list of values to a txt file

    :param string filepath: Filepath for the resulting txt file
    :param list param_list: Content to write in files (each row = a line in the txt file)
    :return: None
    """
    with open(filepath, 'w') as f:
        for row in param_list:
            f.write('{}\n'.format(row))


def action_code_to_speed(action_code: int):
    """
    This function converts the action code to the speed it represents

    :param int action_code: Action code
    :return int: Return the speed limit equivalent to the action_code
    """
    return action_code * 10 + 10
