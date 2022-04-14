import xml.etree.cElementTree as ET
import numpy as np

taz_file = 'tazgrid.add.xml'


def get_tazs(filename):
    root = ET.parse(filename).getroot()
    tazs = {}

    for item in root.findall('taz'):
        taz_id = item.attrib['id']

        sources = []

        for source in item.findall('tazSource'):
            sources.append(source.attrib['id'])

        sinks = []

        for sink in item.findall('tazSink'):
            sinks.append(sink.attrib['id'])

        tazs[taz_id] = (sources, sinks)

    return tazs


tazs = get_tazs(taz_file)

print(tazs)