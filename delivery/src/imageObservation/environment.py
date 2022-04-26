import gym
import action_space
import sumo_event
import reward_function
import environment_actions
import numpy as np

from configuration import Configuration
import state_representation.imageObservations as state_representation

import utils

import os
import sys

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # Checks for the binary in environ vars
import traci


class SUMORLEnvironment(gym.Env):
    """
    This class is used to control the SUMO simulation

    :param Configuration config: Configuration class in order to access the configuration.xml file
    :param string sumo_config_path: Path to the sumo simulation configuration file
    :return: None
    """
    def __init__(self, config: Configuration, sumo_configuration_path: str):
        super().__init__()
        self.config = config

        environment_config = self.config.get(['environment'])

        # SUMO CONFIGURATION
        self.connected = False

        if int(environment_config['sumo_gui']):
            self.sumoBinary = checkBinary('sumo-gui')
        else:
            self.sumoBinary = checkBinary('sumo')

        self.configuration_file = sumo_configuration_path
        self.starting_step = environment_config['starting_step']

        self.simulation_step = 0
        self.traci = traci

        self.event_steps = list(map(int, self.config.get(['event', 'steps']).split()))

        # RL CONFIGURATION
        self.action_space = action_space.single_speed_limit_action_space(config)
        self.state_representation = state_representation.ImageObservations(self.traci, self.config.get(['state_representation', 'image_path']), self.config)
        self.observation_space = self.state_representation.get_observations_size()

        self.seconds_between_actions = int(environment_config['seconds_between_actions'])


    def step(self, action: int):
        """
        This function is called to advance one Reinforcement Learning step in the simulation

        :param int action: Integer value of the action that needs to be taken in the environment
        :return tuple: Returns the RL standard tuple composed of the new state_observation, reward and the done boolean
        """
        # Apply action (here action is the new speed limit)
        if action:
            # Transform action into speed
            speed = utils.action_code_to_speed(action)
            environment_actions.change_global_speed_limit(self.traci, utils.kmh_to_ms(speed))

        # Do as many sumo steps as required between agent action
        for _ in range(0, self.seconds_between_actions):
            self.traci.simulationStep()
            self.state_representation.step(self.simulation_step)

            # Event
            if self.simulation_step in self.event_steps:
                self.step_event()

            self.simulation_step += 1


        state_observation = self.state_representation.get_observations()
        reward = reward_function.compute_reward(traci, self.config.get(['rl', 'reward_function']))

        done = self._traci_not_ended()

        return state_observation, reward, done, {}


    def reset(self):
        """
        This function is used to reset or start the SUMO simulation

        :return np.ndarray: Returns the state_representation at the beginning of the simulation
        """
        if self.connected:
            self.close_connection()
            sys.stdout.flush()

        sumo_command_config = self.config.get(['sumo_command'])

        sumo_cmd = [
            self.sumoBinary,
            "--configuration", self.configuration_file,
        ]

        for key, value in sumo_command_config.items():
            if key == "gui-activated":
                if value == "True":
                    sumo_cmd.extend(['-S', '-Q'])
            else:
                sumo_cmd.extend(['--' + key, value])

        self.traci.start(sumo_cmd)
        self.simulation_step = 0
        self.connected = True

        # Set max speed to initial speed limit
        environment_actions.change_global_speed_limit(self.traci, utils.kmh_to_ms(int(self.config.get(['environment', 'initial_max_speed']))))

        aux = np.array([])
        if self.starting_step:
            aux = self.step(None)[0]
        else:
            aux = self.state_representation.get_observations()

        return aux

        
    def render(self, mode='human', close=False):
        """
        This function is inherited from the gym environment however it is not used

        :return: None
        """
        pass


    def close_connection(self):
        """
        This function is used to close the connection with SUMO

        :return: None
        """
        self.traci.close()
        self.connected = False


    def _traci_not_ended(self):
        """
        Internal function that returns if the SUMO simulation has ended or not

        :return boolean: Returns true if a SUMO simulation is running false otherwise
        """
        simulation_past_end_time = self.simulation_step > int(self.config.get(['environment', 'end_step']))

        return simulation_past_end_time or (self.traci.simulation.getMinExpectedNumber() == 0)



    def get_step(self):
        """
        This function returns the step of the ongoing SUMO simulation

        :return int: Returns the step of the SUMO simulation
        """
        return self.simulation_step


    def step_event(self):
        """
        This function calls at the event function in sumoEvent class

        :param string edge_name: The target edge for the event
        :return: None
        """
        sumo_event.eventBlockEdges(self.traci, self.config.get(['event', 'edge']))


    def get_action_size(self):
        """
        This function return the number of possible actions

        :return int: Returns the number of possible actions
        """
        return self.action_space


    def get_obs_dim(self):
        """
        This function return the dimensions of the observations space

        :return tuple | int: Return the observations dimensions 
        """
        return self.state_representation.get_observations_size()