import xml.etree.cElementTree as ET
import numpy as np

root = ET.Element("routes")


"""
Commnets:
Implement as a function so it can be called in main.py ?
Need parameter route file name to be created
Need information about even going on for route definition (Only block road or more advance event aka School)
"""

"""
Vehicle type information
More attributes available on: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
"""
Vtype_attributes = {
    'id': 'vType1',
    'accel': '2.6', # default 2.6
    'decel': '4.5', # default 4.5
    'sigma': '0.5', # Car following model parameter, default 0.5
    'tau': '1.0', # Car following model parameter, default 1.0
    'speedFactor': 'normc(1, 0.1, 0.2, 2)', # The vehicles expected multiplier for lane speed limits, speedFactor="normc(mean,deviation,lowerCutOff,upperCutOff)"
    'color': '1,1,0', # This vehicle type's color, default Yellow 1,1,0
}

ET.SubElement(root, "vType",
    id=Vtype_attributes['id'],
    accel=Vtype_attributes['accel'],
    decel=Vtype_attributes['decel'],
    sigma=Vtype_attributes['sigma'],
    tau=Vtype_attributes['tau'],
    speedFactor=Vtype_attributes['speedFactor'],
    color=Vtype_attributes['color']
)


"""
Route definition
List of attributes can be found on: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html

Attributes to be implemented:
id .
type .
depart (time)
fromTaz
toTaz

departSpeed = "random"
arrivalSpeed = "current"


viaJunction or via (edge) -> only if special event


color -> for display, not that relevant



Need to adapt to more options.
If no viaJunction/viaEdge -> Can't be from and to same Taz

Change random to normal distribution in case where it better simulates real world.
-> School event: more departure in the early stage as they are going to pickup kids at the school
"""
from_proba = [('Taz1', 0.5), ('Taz2', 1)]
to_proba = [('Taz1', 0.2), ('Taz2', 1)]

delta_time = (0, 3600)

type = Vtype_attributes['id']

num_vehicles = 10
id = 0

for i in range(num_vehicles):
    fromTaz = from_proba[0][0] if np.random.rand() < from_proba[0][1] else from_proba[1][0]
    toTaz = to_proba[0][0] if np.random.rand() < to_proba[0][1] else to_proba[1][0]

    # Maybe better to set a normal distribution
    depart_time = np.random.randint(delta_time[0], delta_time[1])

    idSumo = 'V' + str(id) 
    print('{}, {} to {}, departure: {}'.format(idSumo, fromTaz, toTaz, depart_time))





    id += 1




# tree = ET.ElementTree(root)
# tree.write("TestXML.xml")