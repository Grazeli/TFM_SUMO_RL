#!/usr/bin/env python

import os
import sys
import optparse

# We need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit('Error SUMO_HOME env variable')

from sumolib import checkBinary
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")

    options, args = opt_parser.parse_args()
    return options


test_mode = 1
# TraCI control loop
def run():

    step = 0
    # If things are still going
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # Try rerouting
        if step == 50:
            lane_id = traci.edge.getLaneNumber('e7-1')
            print(lane_id)

            traci.lane.setDisallowed('e7-0_0', ['passenger'])
            # Need to reroute vehicles.

            #traci.vehicle.changeTarget("flow_0.0", "start")
            #traci.vehicle.changeTarget("flow_0.1", "start")
        step+=1

    traci.close()
    sys.stdout.flush()

# main
if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "test_sumo.sumocfg"])
    run()