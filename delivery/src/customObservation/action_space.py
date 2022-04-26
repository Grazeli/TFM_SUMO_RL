from configuration import Configuration


def single_speed_limit_action_space(config: Configuration):
    """
    Function to compute the number of possible actions

    :param Configuration config: Configuration class in order to access the configuration.xml file
    :return int: The number of actions possible for the RL agent
    """
    config_action = config.get(['action_space_range'])
    min = int(config_action['min'])
    max = int(config_action['max'])

    actions = list(range(min, max + 10, 10))
    return len(actions)