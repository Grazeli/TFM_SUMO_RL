import numpy as np
import xml.etree.ElementTree as ET
from observations import Observations
import auxiliary_functions


class EdgeAnalyticsObservations(Observations):
    """
    Class that computes the observations with data obtained from the sumo simulation
    Here we give the agent the following information:
    per edge: # vehicles, std, min, max, avg speed, blocked


    :param library Traci: traci library to access the SUMO simulation
    :param Configuration config: Configuration class in order to access the configuration.xml file
    :return: None
    """
    def __init__(self, traci, config):
        super().__init__(traci)

        self.config = config

        self.junctions_to_edges = {}
        self.edge_info = {}
        self.edge_step_info = {}
        self.num_lanes = {}
        self.blocked = {}
        self.edge_list = []
        self.vehicle_speed = []

        self._precompute_observations()

    
    def _precompute_observations(self):
        """
        Parses the network file in order to set all the attributes to later compute the observations

        :return: None
        """
        network_file = '{}{}'.format(self.config.get(['random_trips', 'folder']), self.config.get(['sumo_configuration', 'net-file']))

        root = ET.parse(network_file).getroot()        

        for item in root:
            # Targetting junctions
            if item.tag == 'connection' and item.attrib['from'][0] == ':':
                self.junctions_to_edges[item.attrib['from']] = item.attrib['to']

            elif item.tag == 'edge' and not 'function' in item.attrib:
                self.edge_info[item.attrib['id']] = []
                self.edge_step_info[item.attrib['id']] = []
                self.edge_list.append(item.attrib['id'])

                self.num_lanes[item.attrib['id']] = len(item)
                self.blocked[item.attrib['id']] = 0


    def _cleanup(self):
        """
        Internal function to cleanup after the computation of the observations

        :return: None
        """
        pass


    def _get_edge(self, name: str):
        """
        Return the edge in which the name is situated, this is done to avoid the junctions
        In the case where the name is a junction it will return the edge where that junction ends

        :param str name: name of the road in the network
        :return str: returns a valid edge of the network 
        """
        if name in self.edge_list:
            return name
        elif name in self.junctions_to_edges:
            return self.junctions_to_edges[name]
        else:
            print('Car road not in edges !')
            return None


    def _compute_observations(self):
        """
        Internal function to compute the observations

        :return: The state representation / observations and the vehicle speeds
        """
        obs = []

        for key, item in self.edge_info.items():
            vehicles_count, speed = zip(*item)

            sum_vehicles = np.sum(vehicles_count)
            max_vehicles = np.max(vehicles_count)
            min_vehicles = np.min(vehicles_count)
            std_vehicles = np.std(vehicles_count)
            

            average_speed = np.sum(speed) / len(speed)

            obs.extend([sum_vehicles, max_vehicles, min_vehicles, std_vehicles, average_speed, self.num_lanes[key], self.blocked[key]])

            # Cleaning for next step
            self.edge_info[key] = []

        tmp = self.vehicle_speed
        self.vehicle_speed = []

        return obs, tmp


    def step(self, step: int):
        """
        Function called at each time step, required for some computation

        :param int step: The sumo simulation step
        :return: None
        """
        ids_cars = self.traci.vehicle.getIDList()

        for car in ids_cars:
            edge = self._get_edge(self.traci.vehicle.getRoadID(car))
            speed =  auxiliary_functions.ms_to_kmh(self.traci.vehicle.getSpeed(car))
            
            self.vehicle_speed.append(speed)

            self.edge_step_info[edge].append(speed)

        # edge_step_info -> edge_info
        for key in self.edge_info.keys():
            if key in self.edge_step_info and len(self.edge_step_info[key]) > 0:
                num_cars = len(self.edge_step_info[key])
                avg_speed = np.sum(self.edge_step_info[key]) / num_cars

                self.edge_info[key].append((num_cars, avg_speed))
            else:
                self.edge_info[key].append((0, 0))

            # Cleaning for next step
            self.edge_step_info[key] = []

    
    def get_observations_size(self):
        """
        Function returning (if possible) the dimensions of the observations.
        It is possible that the program doesn't have that information due to the fact that we can't
        precompute it before having a example. (See report)

        :return: Either the observations shape or None if it is unknown
        """
        # Per edge: # vehicles, std, min, max, avg speed, num_lanes, blocked
        return len(self.edge_list) * 7


    def get_observations(self):
        """
        Function that returns the observations computed

        :return: The state representation / observations
        """
        return self._compute_observations()


    def blocked_route(self, edge: str):
        """
        Functions to update the blocked attribute after an event

        :param string edge: Id of the edge that is being blocked
        :return: None
        """
        for e in edge.split():
            if e in self.blocked:
                self.blocked[e] = 1

