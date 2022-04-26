import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.layers as layers
from tensorflow.keras.optimizers import Adam

from configuration import Configuration


class DQN:
    """
    This class implements the Reinforcement Learning DQN algorithm and represents the RL agent

    :param int | tuple state_size: The size of the 
    :param int action_size: The number of actions available to the agent
    :param int batch_size: Batch size for the neural network training
    :param Configuration config: Configuration class in order to access the configuration.xml file
    :return: None
    """
    def __init__(self, state_size, action_size: int, batch_size: int, config: Configuration):
        self.action_size = action_size
        self.state_size = state_size
        self.batch_size = batch_size
        self.config = config

        agent_config = config.get(['agent'])

        # Parameters:
        self.learning_rate = float(agent_config['learning_rate'])
        self.gamma = float(agent_config['gamma'])
        self.exploration_proba = 1.0
        self.exploration_proba_decay = float(agent_config['exploration_proba_decay'])

        self.memory_buffer = list()
        self.max_memory_buffer = int(agent_config['memory_size'])

        self.model = self.define_model()

    
    def define_model(self):
        """
        Function to define the agent neural network in this case a simple neural network

        :return: None
        """
        inputs = keras.Input(self.state_size)
        
        x = layers.Dense(units=64, activation='relu')(inputs)
        x = layers.Dense(units=64, activation='relu')(x)
        x = layers.Dense(units=24, activation='relu')(x)
        # x = layers.Dropout(0.3)(x)

        outputs = layers.Dense(units=self.action_size, activation='linear')(x)

        model = keras.Model(inputs, outputs, name="dqn_nn")
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate), metrics=['acc'])

        return model


    def compute_action(self, current_state: np.ndarray):
        """
        Function to select the next agent action

        :param np.ndarray current_state: Current simulation state on which the selected action will take place
        :return int: Returns the index of the action the agent took
        """
        if np.random.uniform(0, 1) < self.exploration_proba:
            return np.random.choice(range(self.action_size))

        q_values = self.model.predict(current_state)[0]

        return np.argmax(q_values)


    def update_exploration_proba(self):
        """
        Function to update the exploration probability in order to during the execution slowly move from random actions
        to predicted actions.

        :return: None
        """
        self.exploration_proba = self.exploration_proba * np.exp(-self.exploration_proba_decay)
        print('Updating exploration proba: {}'.format(self.exploration_proba))
        print(self.exploration_proba)


    def store_episode(self, current_state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        """
        Function to store an episode into the agent memory. An episode is composed of the current state (prior to the action),
        the action taken, the reward obtained, and the next state (after the action is done) and the done boolean to know if the episode has ended.

        :param np.ndarray current_state: Simulation state prior to the action
        :param int action: Action taken for the current state
        :param float reward: Reward obtained after the action
        :param np.ndarray next_state: Simulation state after the action is applied to the current state
        :param bool done: If the episode/simulation has ended
        :return: None
        """
        self.memory_buffer.append({
            'current_state': current_state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'done': done,
        })

        if len(self.memory_buffer) > self.max_memory_buffer:
            self.memory_buffer.pop(0)


    def train(self):
        """
        Function to train the agent neural network

        :return: None
        """
        print('Training of the agent')
        np.random.shuffle(self.memory_buffer)
        batch_sample = self.memory_buffer[0:self.batch_size]

        for experience in batch_sample:
            q_current_state = self.model.predict(experience['current_state'])
            q_target = experience['reward']

            if not experience['done']:
                q_target = q_target + self.gamma * np.max(self.model.predict(experience['next_state'])[0])

            q_current_state[0][experience['action']] = q_target

            self.model.fit(experience['current_state'], q_current_state, verbose=0)