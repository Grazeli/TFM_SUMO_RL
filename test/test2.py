import traci

def testfunction():
    print('Import all good')


def eventBlockRoute(traci):
    edge_name1 = 'E26'
    edge_name2 = 'E31'
    for n in range(traci.edge.getLaneNumber(edge_name1)):
                traci.lane.setAllowed(edge_name1 + "_" + str(n), [])

    for n in range(traci.edge.getLaneNumber(edge_name2)):
        traci.lane.setAllowed(edge_name2 + "_" + str(n), [])


def printInformation(traci, step):

    vehiclesID = traci.vehicle.getIDList()

    if len(vehiclesID) > 0:
        num_vehicles = len(vehiclesID)

        speed_average = sum([traci.vehicle.getSpeed(id) for id in vehiclesID]) / num_vehicles

        print('Step: {}, # Vehicles: {}, speed: {}'.format(step, num_vehicles, speed_average))