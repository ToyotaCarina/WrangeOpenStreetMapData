# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import global_funcs as gf

streetname_re = r'^[a-zA-Z øæåØÆÅ]+$' #First suggestion
streetname_re = r'^[a-zA-Z øæåØÆÅ.é]+$'

def audit_streetname(doubtful_streetnames, street_name):
    if not re.search(streetname_re, street_name):
        gf.add_to_array(street_name, doubtful_streetnames)

def print_audit_results(doubtful_streetnames):
    print('\nProblem with data - street names:')
    for item in doubtful_streetnames:
        print item    

def audit(osmfile):
    doubtful_streetnames = []
    with open(osmfile, 'r') as xml_file:
        for event, elem in ET.iterparse(xml_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    k = tag.attrib['k'].encode('utf-8')
                    v = tag.attrib['v'].encode('utf-8')
                    if k == "addr:street":
                        audit_streetname(doubtful_streetnames, v)
                    
    xml_file.close()
    print_audit_results(doubtful_streetnames)

        
if __name__ == '__main__':
    audit(gf.OSM_FILE)
