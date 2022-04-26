import matplotlib.pyplot as plt

plot_reward = True
plot_speed = True

reward_function_is_speed = False

folder = 'exVehiclesSum6544'
episode = 499
filename = '{}/result/result_ep{}.txt'.format(folder, episode)



with open(filename) as f:
    lines = list(f)

results = []

for x in lines:
    # Clear rows
    cleaned_str = x.replace('(', '').replace(')', '').replace(',', '')
    aux = cleaned_str.split()

    if reward_function_is_speed:
        results.append((int(aux[0]), int(aux[1]), float(aux[2])))
    else:
        results.append((int(aux[0]), int(aux[1]), - float(aux[2])))


step, speed, reward = zip(*results)

if plot_speed:
    plt.plot(step, speed, label='speed')

if plot_reward:
    plt.plot(step, reward, label='reward')
plt.legend()
plt.title('Obtained values within episode {}'.format(episode))
plt.show()
