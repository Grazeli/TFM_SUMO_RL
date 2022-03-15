action_space_range = dict(
    min = 10,
    max = 50,
    step = 5,
)


# SUMO RELATED
sumo_gui = False

sumo_directory = 'sumo/'
sumo_configuration_file = 'demo_circle.sumocfg'
sumo_network_file = 'circle_network.net.xml'
sumo_route_file = 'odtrips_valid.xml'


# Initial settings
initial_max_speed = 50
seconds_between_actions = 60