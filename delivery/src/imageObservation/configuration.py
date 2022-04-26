import xml.etree.cElementTree as ET

class Configuration():
    """
    This class is used to read and access the simulation xml configuration file

    :param string filepath: Filepath to the xml configuration file 
    :return: None
    """
    def __init__(self, filepath: str):
        self.root = ET.parse(filepath).getroot()
        self.configuration = self._recursive_make_dict(self.root)


    def _recursive_make_dict(self, recursive_root):
        """
        Internal function called recursively in order to convert the xml tree into a python dictionary

        :param recursive_root: Root of the current tree thats need to be processed into the configuration dictionary
        :return dict: Returns the dictonary resulting from the tree 
        """
        if len(recursive_root) > 0:
            res = {}
            for item in recursive_root:
                res[item.tag] = self._recursive_make_dict(item)

            return res
        else:
            return recursive_root.attrib['value']


    def get(self, keys: list):
        """
        This function returns a part or the whole configuration dictionary depending on the keys given

        :param list keys: List of keys within the configuration file to access the wanted information
        :return dict: Returns part of the configuration dictionary according to the keys given
        """
        dic = self.configuration

        for key in keys:
            if key in dic.keys():
                dic = dic[key]
            else:
                raise Exception('Configuration key does not exist')
        
        return dic
                

        
        
