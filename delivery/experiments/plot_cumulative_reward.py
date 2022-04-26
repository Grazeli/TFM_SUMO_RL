import matplotlib.pyplot as plt

folder = 'exAnalyticsCumulative6225'
reward_function_is_speed = False
num_episodes = 500



final_folder = '{}/result/'.format(folder)
x = list(range(num_episodes))

cumulative_rewards = []

for ep in x:
    filename = '{}result_ep{}.txt'.format(final_folder, str(ep))

    with open(filename) as f:
        lines = list(f)

    results = []

    for l in lines:
        # Clear rows
        cleaned_str = l.replace('(', '').replace(')', '').replace(',', '')
        aux = cleaned_str.split()

        if reward_function_is_speed:
            results.append((int(aux[0]), int(aux[1]), float(aux[2])))
        else:
            results.append((int(aux[0]), int(aux[1]), - float(aux[2])))


    step, speed, reward = zip(*results)

    cumulative_rewards.append(sum(reward))

plt.plot(x, cumulative_rewards, label='cumulative rewards')
plt.title('Cumulative reward per episode')
plt.legend()
plt.show()
