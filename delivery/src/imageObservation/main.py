import configuration
import generateTrips
import generateConfig
import mainLoop

# Parameters
configuration_file = "configuration.xml"


# Configuration part
configurationClass = configuration.Configuration(configuration_file)

print('Configuration loaded')
# Generate routes if needed

sumo_configuration = configurationClass.get(['sumo_configuration'])
if sumo_configuration['route-file']:
    route_file = sumo_configuration['route-file']
    print('Route file loaded')
else:
    route_file = generateTrips.generateTrips(configurationClass, sumo_configuration['net-file'])
    print('Route file generated')

# Generating SUMO configuration file
config_path = generateConfig.generateSumoConfiguration(configurationClass, route_file)

print('Configuration generated')
# Call main loop
mainLoop.mainLoop(configurationClass, config_path)
