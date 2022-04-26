def compute_reward(traci, function_name: str):
    """
    This function is called to select correct reward function

    :param library traci: Library to access the sumo simulation
    :param string function_name: Name of the function to be used to compute the reward
    :return float: Returns the computed reward
    """
    if function_name == 'cumulative_waiting_time':
        return reward_cumulative_waiting_time(traci)


def reward_cumulative_waiting_time(traci):
    """
    This function computes the reward as the average accumulated waiting time per car for the last iteration.
    The reward is negated as we which to reduce the cumulative waiting time.

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