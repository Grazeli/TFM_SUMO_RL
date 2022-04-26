def eventBlockEdges(traci, edge_list: str):
    """
    This function blocks an edge, not allowing cars within it.

    :param library traci: Library to access the sumo simulation
    :param string edge_list: Name of the edges to block
    :return: None
    """
    for edge_name in edge_list.split():
        for n in range(traci.edge.getLaneNumber(edge_name)):
                    traci.lane.setAllowed(edge_name + "_" + str(n), [])


def eventSchoolEdge(traci, edge_name: str):
    """
    This function simulates the school event

    :param library traci: Library to access the sumo simulation
    :param string edge_list: Name of the edges to block
    :return: None
    """
    pass