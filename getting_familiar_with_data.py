## getting familiar with data
show_number_of_rows = 10

import global_funcs as gf
import xml.etree.ElementTree as ET
from pprint import pprint

def count_tags(filename):
    tags={}
    keys={}
    i = 0
    for event, elem in ET.iterparse(filename):
        if type(elem.tag)=='None':
            pass
        gf.add_to_dict(elem.tag, tags)    
        if elem.tag =='tag':
            gf.add_to_dict(elem.attrib['k'], keys)
        # printing some data at the same time           
        if i < show_number_of_rows:
            pprint(ET.tostring(elem, encoding='utf-8'))
        i += 1
    return tags, keys

def print_tags(title, tags):
    print ('\n' + title)
    pprint (tags)

if __name__ == "__main__":
    print('\nPrinting ' + str(show_number_of_rows) + ' rows')
    tags, keys = count_tags(gf.OSM_FILE) 
    print_tags('Number of different tags in the map file:', tags)
    top_used_keys = sorted(keys.iteritems(), key=lambda (k, v): (-v, k))[:10]
    print_tags('Top 10 most used keys:', top_used_keys)
