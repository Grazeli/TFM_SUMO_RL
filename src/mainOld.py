import environment
import agent
import numpy as np

env = environment.SUMORLEnvironment()

n_episodes = 5

max_iterations_ep = 500

batch_size = 32

edge_name1 = 'E26'
edge_name2 = 'E31'

state_size = env.get_obs_dim()
action_size = env.get_action_size()

agent = agent.DQN(state_size, action_size, batch_size)
total_steps = 0

print('Start')
for e in range(n_episodes):
    print('New reset')
    current_state = env.reset()

    current_state = np.append(current_state['network'], current_state['cars'])

    for step in range(max_iterations_ep):
        print('step')
        total_steps += 1

        if env.get_step() > 50:
            env.do_event(edge_name1)
            env.do_event(edge_name2)

        action = agent.compute_action(current_state)

        next_state, reward, done, _ = env.step(action)

        next_state = np.append(next_state['network'], next_state['cars'])

        agent.store_episode(current_state, action, reward, next_state, done)

        if done:
            agent.update_exploration_proba()
            break

        current_state = next_state

    if total_steps >= batch_size:
        agent.train()


env.close_connection()
print("Done")

