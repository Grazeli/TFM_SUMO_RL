from gym import spaces
import config_environment
import numpy as np
import xml.etree.ElementTree as ET

class stateRepresentation():
    def __init__(self) -> None:
        pass

    def observations_format(self):
        """
        Explanation
        :param :
        :return: 
        """
        raise NotImplementedError

    def get_observations(self):
        """
        Compute observations content at a given state
        """
        raise NotImplementedError

    def _precompute_network_representation(self):
        """
        """
        raise NotImplementedError


class stateFirstTest(stateRepresentation):
    def __init__(self, traci) -> None:
        self._traci = traci
        self._directory = config_environment.sumo_directory
        self._network_representation = self._precompute_network_representation()
        self._cars_ids = self._get_car_ids()


    def get_state_representation_dim(self):
        cars = self._compute_cars_observations()

        mixed = np.append(self._network_representation, cars)
        mixed = np.reshape(mixed, (-1, 1))
        return mixed.shape[0]





    def observations_format(self):
        return spaces.Box(low = 0, high=1000000, shape=(2,))

    def get_observations(self):
        aux = self._compute_cars_observations()

        obs = {'network': self._network_representation, 'cars': aux}

        return obs

    """
        x       ID  inNetwork   speed   position
        Cars   x   x            x       x
        """
    def _compute_cars_observations(self):
        vehicle_in_simulation = self._traci.vehicle.getIDList()

        cars_representation = np.empty((0,4))

        for x in self._cars_ids:
            if x in vehicle_in_simulation:
                car_info = [x, 1, self._traci.vehicle.getSpeed(x), self._traci.vehicle.getRoadID(x)]

            else:
                car_info = [x, 0, 0, '']

            cars_representation = np.append(cars_representation, np.array([car_info]), axis=0)

        return cars_representation


    def _precompute_network_representation(self):
        network_file = self._directory + config_environment.sumo_network_file

        root = ET.parse(network_file).getroot()

        network_representation = np.empty((0, 4))

        """
        x       ID  FROM    TO  NB_LANES
        Edges   x   x       x   x
        """
        for x in root.findall('edge'):

            if 'from' in x.attrib:
                array = [x.attrib['id'], x.attrib['from'], x.attrib['to'], len(list(x.findall('lane')))]
                network_representation = np.append(network_representation, np.array([array]), axis=0)

        return network_representation

    def _get_car_ids(self):
        route_file = self._directory + config_environment.sumo_route_file

        root = ET.parse(route_file).getroot()

        cars_ids = []

        for x in root.findall('trip'):
            cars_ids.append(x.attrib['id']) 

        return cars_ids