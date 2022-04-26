from configuration import Configuration
import numpy as np

def compute_reward(traci, function_name: str, config: Configuration, speed_list: list):
    """
    This function is called to select correct reward function

    :param library traci: Library to access the sumo simulation
    :param string function_name: Name of the function to be used to compute the reward
    :param Configuration config: Configuration class in order to access the configuration.xml file
    :param list speed_list: List that contains the average speed of every edge during the last step
    :return float: Returns the computed reward
    """
    if function_name == 'avg_waiting_time':
        return reward_avg_cumulative_waiting_time(traci)
    elif function_name == 'average_speed':
        return reward_average_speed(speed_list)
    elif function_name == 'sum_waiting_time':
        return sum_cumulative_waiting_time(traci)


def reward_avg_cumulative_waiting_time(traci):
    """
    This function computes the reward as the average accumulated waiting time per car for the last iteration
    The reward is negated as we which to reduce the cumulative waiting time

    :param library traci: Library to access the sumo simulation
    :return float: Returns the computed reward
    """
    vehicle_in_simulation = traci.vehicle.getIDList()

    if len(vehicle_in_simulation) > 0:
        total_waiting_time = 0
        for v in vehicle_in_simulation:
            total_waiting_time += traci.vehicle.getAccumulatedWaitingTime(v)
    
        return - (total_waiting_time / len(vehicle_in_simulation))

    else:
        return 0


def sum_cumulative_waiting_time(traci):
    """
    This function computes the reward as the sum of all the cars within the simulation accumulated waiting time since the last iteration
    The reward is negated as we which to reduce it

    :param library traci: Library to access the sumo simulation
    :return float: Returns the computed reward
    """
    vehicle_in_simulation = traci.vehicle.getIDList()

    total_waiting_time = 0
    for v in vehicle_in_simulation:
        total_waiting_time += traci.vehicle.getAccumulatedWaitingTime(v)
    
    return - total_waiting_time


def reward_average_speed(speed_list: list):
    """
    This function computes the reward as the average speed per car for tthe last iteration
    In this case it is not negated as we wich to maximize it

    :param list speed_list: List that contains the average speed of every edge during the last step
    :return float: Returns the computed reward
    """
    return np.sum(speed_list) / len(speed_list)