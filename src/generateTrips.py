import subprocess
import configuration


def generateTrips(configuration: configuration.Configuration, net_file):
    """
    This function calls the SUMO randomTrips scrip to generate the route files for the traffic in our simulation.
    All the parameters from this functions are obtained through the configuration class thus from the configuration.xml file (subsecttion 'random_trips').

    :param Configuration configuration: Configuration class in order to access the configuration.xml file
    :param string net_file: Path to the simulation network
    :return: returns the path to the route file generated
    """
    config = configuration.get(['random_trips'])

    command = [config['command'], config['path'], "--net-file", config['folder'] + net_file]
    command.append('--random')

    for key, value in config.items():
        if key != "command" and key != "path" and key != "folder":
            command.extend(["--" + key, value])

    print('Start command:', command)
    subprocess.run(command)
    print('Ended')

    return config['route-file'].split('/')[-1]