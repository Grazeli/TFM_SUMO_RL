import os
import sys

import observations
import testing
import reward

# Move to config file
configuration_file = "demo_circle.sumocfg"
step_duration = 1 # In seconds

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # Checks for the binary in environ vars
import traci

pwd = '/Users/gazelpaul/TFM/TFM_SUMO_RL/test'

# TraCI control loop
def run():
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()

        if step == 30:
            print('\n--------------\n')
            edges = traci.edge.getIDList()
            for eid in edges:
                for i in range(traci.edge.getLaneNumber(eid)):
                    links = traci.lane.getLinks(eid + '_' + str(i))
                    
                    for l in links:
                        print(l)



        step += 1

        if step == 60:
            break

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')

    sumo_cmd = [
        sumoBinary,
        "-c", configuration_file,
        '--ignore-route-errors', 'True',
        '--device.rerouting.probability', '0.25',
        '--device.rerouting.period', '1',
        '--device.rerouting.synchronize','True',
        '--device.rerouting.threads', '8',
        '-S', '-Q',
    ]

    traci.start(sumo_cmd)

    run()