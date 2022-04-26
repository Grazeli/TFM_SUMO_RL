def change_global_speed_limit(traci, max_speed):
    """
    Function to change the speed limit within the simulation

    :param library Traci: Library in order to access the sumo simulation
    :param float max_speed: Speed limit to set within the simulation
    :return: None
    """
    for e in traci.edge.getIDList():
        traci.edge.setMaxSpeed(e, max_speed)