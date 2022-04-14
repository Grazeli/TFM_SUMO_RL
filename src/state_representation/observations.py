import numpy as np

class Observations():
    """
    Base class for the state representation / observations class for Reinforcement Learning

    :param library traci: The traci library
    :return: None
    """
    def __init__(self, traci):
        self.traci = traci
        self.observations = np.array([])

    def _cleanup(self):
        """
        Internal function to cleanup after the computation of the observations

        :return: None
        """
        pass

    def _compute_observations(self):
        """
        Internal function to compute the observations

        :return: The state representation / observations
        """
        pass

    def step(self, step):
        """
        Function called at each time step, required for some observations implementation

        :param int step: The sumo step
        :return: None
        """
        pass

    def get_observations_size(self):
        """
        Function that returns the dimensions of the observations

        :return: Returns the dimensions of the observations
        """
        return None

    def get_observations(self):
        """
        Function that returns the observations computed

        :return: The state representation / observations
        """
        return self._compute_observations()
