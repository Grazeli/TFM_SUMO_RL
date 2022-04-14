import gym
import action_space
import sumo_event
import reward_function
import environment_actions

import configuration
import state_representation.imageObservations as state_representation

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


class SUMORLEnvironment(gym.Env):
    """
    This class is used to control the SUMO environment

    :param Configuration config: Configuration class in order to access the configuration.xml file
    :param string sumo_config_path: Path to the sumo simulation configuration file
    :return:
    """
    def __init__(self, config: configuration.Configuration, sumo_configuration_path):
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

        # RL CONFIGURATION
        self.action_space = action_space.single_speed_limit_action_space(config)
        
        self.state_representation = state_representation.ImageObservations(self.traci, self.config.get(['state_representation', 'image_path']))
        self.observation_space = self.state_representation.get_observations_size()

        self.seconds_between_actions = int(environment_config['seconds_between_actions'])


    def step(self, action):
        """
        This function is called to advance one Reinforcement Learning step in the simulation

        :param int action: Integer value of the action that needs to be taken in the environment
        :return tuple: Returns the RL standard tuple composed of the new state_observation, reward and the done boolean
        """
        # Apply action (here action is the new speed limit)
        if action:
            # Transform action into speed
            speed = action * 10 + 10
            environment_actions.change_global_speed_limit(self.traci, utils.kmh_to_ms(speed))

        # Do as many sumo steps as required between agent action
        for _ in range(0, self.seconds_between_actions):
            self.traci.simulationStep()
            self.state_representation.step(self.simulation_step)
            self.simulation_step += 1


        state_observation = self.state_representation.get_observations()
        reward = self.compute_reward()

        done = not self.traci_not_ended()

        # return obs, reward, done, {}
        return state_observation, reward, done, {}


    def reset(self):
        """
        This function is used to reset or start the SUMO simulation

        :return Observations: Returns the state_representation at the beginning of the simulation
        """
        if self.connected:
            self._close_connection()


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

        print(sumo_cmd)
        self.traci.start(sumo_cmd)
        self.connected = True

        # Set max speed to initial speed limit
        environment_actions.change_global_speed_limit(self.traci, utils.kmh_to_ms(int(self.config.get(['environment', 'initial_max_speed']))))

        if self.starting_step:
            self.step(None)

        return self.state_representation.get_observations()

        
    def render(self, mode='human', close=False):
        """
        This function is inherited from the gym environment however it is not used

        :return: None
        """
        pass


    def _close_connection(self):
        """
        This function is used to close the connection with SUMO

        :return: None
        """
        self.traci.close()
        self.connected = False


    def traci_not_ended(self):
        """
        This function returns if the SUMO simulation has ended or not

        :return boolean: Returns true if a SUMO simulation is running false otherwise
        """
        return self.traci.simulation.getMinExpectedNumber() > 0


    def get_step(self):
        """
        This function returns the step of the ongoing SUMO simulation

        :return int: Returns the step of the SUMO simulation
        """
        return self.simulation_step


    def do_event(self, edge_name):
        """
        This function calls at the event function in sumoEvent class

        :param string edge_name: The target edge for the event
        :return: None
        """
        # May need redo?
        sevent = sumo_event.sumoEvent(self.traci)
        sevent.eventBlockEdge(edge_name)


    def compute_reward(self):
        """
        This function is called to compute the reward

        :return float: Returns the computed reward
        """
        vehicle_in_simulation = self.traci.vehicle.getIDList()

        if len(vehicle_in_simulation) > 0:
            total_waiting_time = 0
            for v in vehicle_in_simulation:
                total_waiting_time += self.traci.vehicle.getAccumulatedWaitingTime(v)
            
            return total_waiting_time / len(vehicle_in_simulation)

        else:
            return 0


    def get_action_size(self):
        """
        This function return the number of possible actions

        :return int: Returns the number of possible actions
        """
        return self.action_space


    def get_obs_dim(self):
        """
        This function return the dimensions of the observations space

        :param string recursive_root: Root of the current tree thats need to be processed into the configuration dictionary
        :return dict: Returns the dictonary resulting from the tree given 
        """
        return self.state_representation.get_observations_size()