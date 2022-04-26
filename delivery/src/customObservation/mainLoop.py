from configuration import Configuration
import environment
import agent as agentClass
import numpy as np
import utils
import time
import sys


def mainLoop(config: Configuration, sumo_config_path: str):
    """
    This function consists of the main loop of the reinforcement learning algorithm

    :param Configuration config: Configuration class in order to access the configuration.xml file
    :param string sumo_config_path: Path to the sumo simulation configuration file
    :return: None
    """
    env = environment.SUMORLEnvironment(config, sumo_config_path)

    result_folder = config.get(['result', 'folder'])

    rl_config = config.get(['rl'])

    n_episodes = int(rl_config['n_episodes'])
    max_iterations_ep = int(rl_config['max_iterations_ep'])
    batch_size = int(rl_config['batch_size'])

    state_size = env.get_obs_dim()
    action_size = env.get_action_size()

    agent = agentClass.DQN(state_size, action_size, batch_size, config)
    total_step = 0

    start_time = time.clock()
    for e in range(n_episodes):
        print('Start episode {}'.format(e))
        results = []

        current_state = env.reset()
        
        current_state = np.array([current_state])

        for step in range(max_iterations_ep):
            total_step += 1

            action = agent.compute_action(current_state)

            next_state, reward, done, _ = env.step(action)

            next_state = np.array([next_state])

            agent.store_episode(current_state, action, reward, next_state, done)

            if done:
                agent.update_exploration_proba()
                break
        
            current_state = next_state

            results.append((step, utils.action_code_to_speed(action), reward))

        if total_step >= batch_size:
            agent.train()

        utils.write_in_txt(result_folder + '/result_ep{}.txt'.format(e), results)

    env.close_connection()
    print('Execution time: {} seconds'.format(time.clock() - start_time))
    sys.stdout.flush()
    