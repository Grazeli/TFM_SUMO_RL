from distutils.command.config import config
import gym
import action_space
import state_representation
import config_environment
import sumo_event
import reward_function
import environment_actions

import utils

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # Checks for the binary in environ vars
import traci



"""
"""
class SUMORLEnvironment(gym.Env):
    
    def __init__(self, start=0) -> None:
        super().__init__()

        # SUMO CONFIGURATION
        self._connected = False

        if config_environment.sumo_gui:
            self._sumoBinary = checkBinary('sumo-gui')
        else:
            self._sumoBinary = checkBinary('sumo')

        self._configuration_file = config_environment.sumo_directory + config_environment.sumo_configuration_file
        self._step_duration = 1 # In seconds

        
        self._start = start
        self._step = start
        self._traci = traci

        # RL CONFIGURATION
        
        self._action_space = action_space.single_speed_limit_action_space()
        
        self._state_representation = state_representation.stateFirstTest(self._traci)
        self._observation_space = self._state_representation.observations_format()

        self.reset()


    """
    """
    def step(self, action):
        # Apply action (here action is the new speed limit)

        # Transform action into speed
        speed = action * 10 + 10
        environment_actions.change_global_speed_limit(self._traci, utils.kmh_to_ms(speed))

        # Do as many sumo steps as required between agent action
        for _ in range(0, config_environment.seconds_between_actions):
            self._traci.simulationStep()
            self._step += 1


        state_observation = self._state_representation.get_observations()
        reward = self.compute_reward()

        done = not self.traci_not_ended()

        # return obs, reward, done, {}
        return state_observation, reward, done, {}



    """
    """
    def reset(self):
        if self._connected:
            self.close_connection()
            self._connected = False

        # options: --tripinfo-output & tripinfo.xml
        sumo_cmd = [
            self._sumoBinary,
            "-c", self._configuration_file,
            '--ignore-route-errors', 'True',
            '--device.rerouting.probability', '0.25',
            '--begin', str(self._start),
            '--device.rerouting.period', '1',
            '--device.rerouting.synchronize','True',
            '--device.rerouting.threads', '8',
            '--step-length', str(self._step_duration),
        ]

        self._traci.start(sumo_cmd)
        self._connected = True
        
        # Set max speed to initial speed limit
        environment_actions.change_global_speed_limit(self._traci, utils.kmh_to_ms(config_environment.initial_max_speed))
        
        return self._state_representation.get_observations()

        

    """
    """
    def render(self, mode='human', close=False):
        pass



    """
    """
    def close_connection(self):
        self._traci.close()


    def is_connected(self):
        return self._connected

    def traci_not_ended(self):
        return self._traci.simulation.getMinExpectedNumber() > 0

    def get_step(self):
        return self._step

    def do_event(self, edge_name):
        sevent = sumo_event.sumoEvent(self._traci)

        sevent.eventBlockEdge(edge_name)

    def get_state_size(self):
        return self._observation_space

    def get_action_size(self):
        return self._action_space


    def compute_reward(self):
        vehicle_in_simulation = self._traci.vehicle.getIDList()
        return 0

    def get_obs_dim(self):
        return self._state_representation.get_state_representation_dim()