import config_environment

"""
May need later on to do it in a class
"""
def change_global_speed_limit(traci, max_speed):
    edge_list = traci.edge.getIDList()

    for e in edge_list:
        traci.edge.setMaxSpeed(e, max_speed)