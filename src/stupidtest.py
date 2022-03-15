import config_environment

count = 0

for _ in range(0, config_environment.seconds_between_actions):
    count += 1

print(count)