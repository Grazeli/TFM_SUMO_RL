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
import numpy as np
from DQN.DQN import DQN

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")

    options, args = opt_parser.parse_args()
    return options

# TRACI control loop
def run():
    state_size = ['test'] # Needs to be defined, big point
    action_size = ['test'] # Array 2x#roads one increase one decrease.

    # Parameters need to be defined
    n_episodes = 100
    max_iterations_ep = 2000
    batch_size = 32

    agent = DQN(state_size, action_size, batch_size)

    for e in range(n_episodes):
        # Start/Reset environment
        current_state = 'env_start'

        # TraCI control loop
        step = 0
        # If things are still going
        while traci.simulation.getMinExpectedNumber() > 0 or step < max_iterations_ep:
            action = agent.compute_action(current_state)

            # TRACI apply action
            traci.simulationStep()

            # From TRACI collect next state
            next_state = 'next_state'

            # TRACI compute Reward function -> Maybe over several time step, need to define another loop
            reward = 'reward'

            # is the simulation done ?
            done = not(traci.simulation.getMinExpectedNumber() > 0 or step < max_iterations_ep)

            # Store experience
            agent.store_episode(current_state, action, reward, next_state, done)

            if done:
                agent.update_exploration_proba()

            current_state = next_state

            step+=1

    traci.close()

# main
if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "test_sumo.sumocfg"])
    run()