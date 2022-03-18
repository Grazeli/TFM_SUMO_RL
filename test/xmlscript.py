import xml.etree.ElementTree as ET

mytree = ET.parse('odtrips_valid.xml')
myroot = mytree.getroot()

for x in myroot.findall('trip'):
    print(x.attrib)

print('Done')