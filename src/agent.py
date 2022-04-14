import numpy as np
import gym
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from matplotlib import pyplot as plt

"""
"""
class DQN:
    def __init__(self, state_size, action_size, batch_size) -> None:
        self.action_size = action_size
        self.state_size = state_size
        self.batch_size = batch_size

        # Parameters:
        self.lr = 0.001
        self.gamma = 0.99
        self.exploration_proba = 1.0
        self.exploration_proba_decay = 0.005

        self.memory_buffer = list()
        self.max_memory_buffer = 2000

        if self.state_size:
            self.model = self.define_model()
            self.model_created = True
        else:
            self.model_created = False

    """
    Define and compile deep neural network model
    """
    def define_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim = self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(lr=self.lr))

        return model

    """
    Get next action
    """
    def compute_action(self, current_state):
        if not self.model_created:
            self.state_size = current_state.shape
            self.define_model()

        if np.random.uniform(0, 1) < self.exploration_proba:
            return np.random.choice(range(self.action_size))

        q_values = self.model.predict(current_state)[0]

        return np.argmax(q_values)

    """
    End episode -> update exploration probability
    """
    def update_exploration_proba(self):
        self.exploration_proba = self.exploration_proba * np.exp(-self.exploration_proba_decay)
        # print(self.exploration_proba)

    def store_episode(self, current_state, action, reward, next_state, done):
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
        np.random.shuffle(self.memory_buffer)
        batch_sample = self.memory_buffer[0:self.batch_size]

        for experience in batch_sample:
            q_current_state = self.model.predict(experience['current_state'])
            q_target = experience['reward']

            if not experience['done']:
                q_target = q_target + self.gamma * np.max(self.model.predict(experience['next_state'])[0])

            q_current_state[0][experience['action']] = q_target

            self.model.fit(experience['current_state'], q_current_state, verbose=0)