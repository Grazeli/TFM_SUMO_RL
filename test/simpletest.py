import os
import sys
from io import BytesIO

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

pwd = '/Users/gazelpaul/TFM/test/'

# TraCI control loop
def run():
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()

        if step == 50:

            temp = BytesIO()
            view = 'View #0'

            print(traci.gui.hasView(view))
            print(traci.gui.getBoundary(view))

            #traci.gui.screenshot(view, pwd + 'test.png')

            try:
                traci.gui.screenshot(view, temp)

            except Exception as e:
                print(e)

            temp.seek(0)

            content = temp.getvalue()
            temp.close()

            print(content)
            print('\n---\n')
            print(type(content))

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
        #'--step-length', str(step_duration),
        '-S', '-Q',
    ]

    traci.start(sumo_cmd)

    run()