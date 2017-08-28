from pprint import pprint
import xml.etree.ElementTree as ET
import re
import global_funcs as gf

postcode_re = re.compile(r'^\d{1,4}$', re.IGNORECASE)

def audit_postcode(norwegian_postcodes,doubtful_postcodes, postcode):
    if (not postcode_re.match(postcode)) or (postcode not in norwegian_postcodes):
        gf.add_to_array(postcode, doubtful_postcodes)

def audit_postcode_city(norwegian_postcodes, doubtful_postcodes_cities, postcode, city):    
    if (city == '') and (postcode != ''):
        gf.add_to_array(postcode, doubtful_postcodes_cities['postcode w/empty city'])    
    if (city != '') and (postcode != '') and (city.decode('utf8').lower() != norwegian_postcodes[postcode]): 
        doubtful_postcodes_cities['not matching city postcode'].append([postcode,city])

def audit(osmfile):
    norwegian_postcodes = gf.parse_postcodes_file()
    doubtful_postcodes_cities = {}
    doubtful_postcodes_cities['doubtful postcode'] = []
    doubtful_postcodes_cities['postcode w/empty city'] = []
    doubtful_postcodes_cities['not matching city postcode'] = []
    with open(osmfile, 'r') as xml_file:
        for event, elem in ET.iterparse(xml_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                postcode = ''
                city = ''
                for tag in elem.iter("tag"):
                    k = tag.attrib['k'].encode('utf-8')
                    v = tag.attrib['v'].encode('utf-8')
                    if k == "addr:city":
                        city = v
                    if k == "addr:postcode":
                        postcode = v
                        audit_postcode(norwegian_postcodes,doubtful_postcodes_cities['doubtful postcode'], v)
                audit_postcode_city(norwegian_postcodes, doubtful_postcodes_cities, postcode, city)                                        
    xml_file.close()
    print('\nProblem with data - city and postcode:')
    pprint(doubtful_postcodes_cities)

if __name__ == '__main__':
    audit(gf.OSM_FILE)
