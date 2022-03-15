import config_environment

"""
"""
class sumoEvent:
    def __init__(self, traci) -> None:
        self._traci = traci

    """
    """
    def eventBlockEdge(self, edge_name):
        for n in range(self._traci.edge.getLaneNumber(edge_name)):
                    self._traci.lane.setAllowed(edge_name + "_" + str(n), [])

    """
    """
    def eventSchoolEdge(self, edge_name):
        pass
