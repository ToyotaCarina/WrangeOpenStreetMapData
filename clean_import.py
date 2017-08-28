# -*- coding: utf-8 -*-
## Cleaning data, converting to JSON format, importing to MongoDB
import re
import xml.etree.ElementTree as ET 
import codecs
import json
import global_funcs as gf
   
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def update_streetname(name):
    name = name.replace("'", "")    
    return name

def update_postcode(postcode):
    postcode = re.sub('\D', '', postcode)    
    return postcode

def update_phone(phone_number):
    phone_number = re.sub('^(0047|\+47)|\s|\D', '', phone_number)
    if len(phone_number) == 8:
        if (phone_number[0] == '4') or (phone_number[0] == '9'):
            phone_number = '{} {} {} {}'.format(phone_number[0:2], phone_number[2:4], phone_number[4:6], phone_number[6:])
        else: phone_number = '{} {} {}'.format(phone_number[0:3], phone_number[3:6], phone_number[6:])
    elif len(phone_number) == 6:
        phone_number = '{} {}'.format(phone_number[0:4], phone_number[4:])
    return phone_number

def get_city(postcode):
    return norwegian_postcodes[postcode].title()

def add_city_tag(postcode,city, node):
    #adding city tag if postcode exists, but city value is empty
    if (postcode != '') and (city == ''):
        node['address']['city'] = get_city(postcode).title()

def clean_data(k,val):
    if k == "addr:street":
        val = update_streetname(val)
    elif k == "phone":
        val = update_phone(val)
    elif k == "addr:postcode":
        val = update_postcode(val) 

def shape_element(element):
    node = {}
    node['created'] = {}
    node['address'] = {}
    node['pos'] = [0] * 2
    node['node_refs'] = []
    postcode = ''
    city = ''
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for attrName, attrValue in element.attrib.items():
            if attrName in CREATED:
                node['created'][attrName] = attrValue
                pass
            elif attrName in ['lat', 'lon']:
                if attrName == 'lat':
                        node['pos'][0] = float(attrValue)
                else: node['pos'][1] = float(attrValue)
            else: node[attrName] = attrValue
        for nd in element.iter("nd"):
            node['node_refs'].append(nd.attrib['ref'])
        for tag in element.iter("tag"): 
            k = tag.attrib['k'] 
            val = tag.attrib['v']
            clean_data(k,val)
            if k == "addr:postcode":
                postcode = val
            elif k == "addr:city":
                city = val
            if k.count(':') > 1:
                pass
            elif k.startswith('addr:'):
                k = k.replace('addr:','')
                node['address'][k] = val
            elif ':'in k:
                pass
            else: node[k] = val
        add_city_tag(postcode,city,node) 
        for x in list(node.keys()):
            if (node[x] == {}) or (node[x] == []):
                del node[x]        
        return node
    else:
        return None

def process_map(file_in, file_out, pretty = False):
    data = []    
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
     
def clean_and_import():    
    data = process_map(gf.OSM_FILE,gf.JSON_FILE, True)
    gf.print_file_sizes([gf.OSM_FILE, gf.JSON_FILE]) 
    db = gf.MongoDB_connect()
    gf.MongoDB_insert_data(data, db)
    
if __name__ == '__main__':    
    norwegian_postcodes = gf.parse_postcodes_file()
    clean_and_import()                          

    
