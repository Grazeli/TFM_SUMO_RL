import configuration

filename = "configuration.xml"

config = configuration.ConfigurationVariables(filename)

print(config.get(['action_space_range', 'min']))