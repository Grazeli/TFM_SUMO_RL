import xml.etree.cElementTree as ET
import configuration

def generateSumoConfiguration(configurationClass: configuration.Configuration, route_file):
    """
    This function generates the xml sumo configuration file for the simulation

    :param Configuration configuration: configuration class in order to access the configuration.xml file
    :param string route_file: path 
    :return dict: Returns the path to the generated xml sumo configuration file
    """
    config = configurationClass.get(['sumo_configuration'])
    config_path = config['name']
    
    root = ET.Element("configuration")
    input = ET.SubElement(root, "input")

    ET.SubElement(input, "net-file", value=config['net-file'])
    ET.SubElement(input, "route-files", value=route_file)

    processing = ET.SubElement(root, "processing")

    ET.SubElement(processing, "ignore-route-errors", value="true")

    gui = ET.SubElement(root, "gui_only")

    ET.SubElement(gui, "gui-settings-file", value=config['gui-settings-file'])

    


    tree = ET.ElementTree(root)
    tree.write(config_path)
    return config_path