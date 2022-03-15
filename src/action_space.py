from gym import spaces
import config_environment

def single_speed_limit_action_space():
    min = config_environment.action_space_range['min']
    max = config_environment.action_space_range['max']
    step = config_environment.action_space_range['step']

    actions = list(range(min, max + step, step))
    # spaces.Discrete(5)
    return len(actions)