import subprocess
from configuration import Configuration


def generateTrips(configuration: Configuration, net_file):
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

    for key, value in config['options'].items():
        if key == "output-trip-file" or key == "route-file":
            command.extend(['--' + key, '{}/{}'.format(config['folder'], value)])
        else:
            command.extend(['--' + key, value])
            
    subprocess.run(command)

    return config['options']['route-file']