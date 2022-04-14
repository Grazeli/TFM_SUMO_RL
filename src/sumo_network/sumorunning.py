import os
import sys

# Move to config file
configuration_file = "osm.sumocfg"

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # Checks for the binary in environ vars
import traci

# get path for image
directory_path = os.getcwd()
image_name = "/screenshot.png"
file_path = directory_path + image_name





# TraCI control loop
def run():
    
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()

        vehicle = traci.vehicle.getIDList()

        res = 0
        if len(vehicle) > 0:
            for v in vehicle:
                res += traci.vehicle.getWaitingTime(v)

            res / len(vehicle)

        print(res)



        step += 1

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')
    # sumoBinary = checkBinary('sumo')

    sumo_cmd = [
        sumoBinary,
        "--configuration", configuration_file,
        '--ignore-route-errors', 'True',
        '--device.rerouting.probability', '0.25',
        '--device.rerouting.period', '1',
        '--device.rerouting.synchronize','True',
        '--device.rerouting.threads', '8',
        '--default.carfollowmodel', 'EIDM',
        '-S', '-Q',
        "--ignore-junction-blocker", "100",
        # "--mesosim", "True"
    ]

    traci.start(sumo_cmd)

    run()