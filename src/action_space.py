import configuration

def single_speed_limit_action_space(config: configuration.Configuration):
    config_action = config.get(['action_space_range'])
    min = int(config_action['min'])
    max = int(config_action['max'])
    step = int(config_action['step'])

    actions = list(range(min, max + step, step))
    # spaces.Discrete(5)
    return len(actions)