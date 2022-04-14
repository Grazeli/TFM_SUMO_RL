from nbformat import current_nbformat
import environment
import agent as agentClass
import numpy as np
import configuration


def mainLoop(config: configuration.Configuration, sumo_config_path):
    """
    This function consists of the main loop of the reinforcement learning algorithm

    :param Configuration config: Configuration class in order to access the configuration.xml file
    :param string sumo_config_path: Path to the sumo simulation configuration file
    :return: 
    """
    env = environment.SUMORLEnvironment(config, sumo_config_path)

    rl_config = config.get(['rl'])

    n_episodes = int(rl_config['n_episodes'])
    max_iterations_ep = int(rl_config['max_iterations_ep'])
    batch_size = int(rl_config['batch_size'])

    state_size = env.get_obs_dim()
    action_size = env.get_action_size()

    agent = agentClass.DQN(state_size, action_size, batch_size)
    total_step = 0

    print('Start')
    for e in range(n_episodes):
        print('Start episode')
        current_state = env.reset()

        print(current_state)
        break

        for step in range(max_iterations_ep):
            total_step += 1

            # Do event stuff

            action = agent.compute_action(current_state)

            next_state, reward, done, _ = env.step(action)

            agent.store_episode(current_state, action, reward, next_state, done)

            if done:
                agent.update_exploration_proba()
                break
        
            current_state = next_state

        if total_step >= batch_size:
            agent.train()

    env.close_connection()
    print('Done')
    return []
    