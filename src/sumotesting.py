import os
import sys

import state_representation.imageObservations as observations

import configuration
import generateTrips
import generateConfig
import matplotlib.pyplot as plt

# Parameters
configuration_file = "configurationtesting.xml"


# Configuration part
configurationClass = configuration.Configuration(configuration_file)

print('Configuration loaded')
# Generate routes if needed

sumo_configuration = configurationClass.get(['sumo_configuration'])
if sumo_configuration['route-file']:
    route_file = sumo_configuration['route-file']
else:
    route_file = generateTrips.generateTrips(configurationClass, sumo_configuration['net-file'])

print(route_file)
print('Route generated')
# Generating SUMO configuration file
config_path = generateConfig.generateSumoConfiguration(configurationClass, route_file)

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # Checks for the binary in environ vars
import traci

# get path for image
image_name = "sumo/screenshot.png"
file_path = image_name



def compute_reward():
    """
    This function is called to compute the reward

    :return float: Returns the computed reward
    """
    vehicle_in_simulation = traci.vehicle.getIDList()

    if len(vehicle_in_simulation) > 0:
        total_waiting_time = 0
        for v in vehicle_in_simulation:
            total_waiting_time += traci.vehicle.getAccumulatedWaitingTime(v)
        
        return total_waiting_time / len(vehicle_in_simulation)

    else:
        return 0

# TraCI control loop
def run():
    observationClass = observations.ImageObservations(traci, file_path)
    
    step = 0
    rewards = []

    while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()

        reward = compute_reward()
        rewards.append(reward)
        print('Reward: {}'.format(reward))

        if step == 49:
            observationClass._make_screenshot()

        elif step == 50:
            obs = observationClass.get_observations()

        step += 1

    # Plot rewards
    y = list(range(0, len(rewards)))
    plt.title("Line graph")
    plt.plot(rewards, y, color="red")

    plt.show()
    

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')
    # sumoBinary = checkBinary('sumo')

    sumo_cmd = [
        sumoBinary,
        "--configuration", config_path,
        '--ignore-route-errors', 'True',
        '--device.rerouting.probability', '0.25',
        '--device.rerouting.period', '1',
        '--device.rerouting.synchronize','True',
        '--device.rerouting.threads', '8',
        '-S', '-Q',
    ]

    traci.start(sumo_cmd)

    run()