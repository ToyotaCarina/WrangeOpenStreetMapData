# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import global_funcs as gf
from pprint import pprint

city_re = re.compile(r'^[a-zA-Z øæåØÆÅ]+$')

def audit_city(norwegian_postcodes,doubtful_cities, city):
    if (not city_re.match(city)) or (city.decode('utf8').lower() not in norwegian_postcodes.values()):
        add_to_array(city, doubtful_cities)

def audit(osmfile):
    doubtful_cities = []
    norwegian_postcodes = gf.parse_postcodes_file()
    with open(osmfile, 'r') as xml_file:
        for event, elem in ET.iterparse(xml_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    k = tag.attrib['k'].encode('utf-8')
                    v = tag.attrib['v'].encode('utf-8')
                    if k == "addr:city":
                        audit_city(norwegian_postcodes,doubtful_cities, v)
                    
    xml_file.close()
    print('\nProblem with data - cities:')
    pprint(doubtful_cities)
        
if __name__ == '__main__':
    audit(gf.OSM_FILE)
