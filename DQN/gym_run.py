import gym
import numpy as np
from DQN import DQN


env = gym.make('LunarLander-v2')

state_size = env.observation_space.shape[0]
action_size = env.action_space.n

n_episodes = 100
max_iteration_ep = 500

batch_size = 32

agent = DQN(state_size, action_size, batch_size)
total_steps = 0

for e in range(n_episodes):

    current_state = env.reset()

    current_state = np.array([current_state])

    for step in range(max_iteration_ep):
        total_steps += 1

        action = agent.compute_action(current_state)

        next_state, reward, done, _ = env.step(action)

        next_state = np.array([next_state])

        agent.store_episode(current_state, action, reward, next_state, done)

        if done:
            agent.update_exploration_proba()
            break

        current_state = next_state

    if total_steps >= batch_size:
        agent.train()


# Just for gym
def make_video():
    env_to_wrap = gym.make('LunarLander-v2')
    env = gym.wrappers.Monitor(env_to_wrap, 'videos', force = True)

    rewards = 0
    steps = 0
    done = False
    state = np.array([env.reset()])

    while not done:
        action = agent.compute_action(state)
        state, reward, done, _ = env.step(action)
        state = np.array([state])

        steps += 1
        rewards += reward

    print(rewards)
    env.close()
    env_to_wrap.close()

make_video()
