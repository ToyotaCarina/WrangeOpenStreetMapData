from pprint import pprint
import xml.etree.ElementTree as ET
import re
import global_funcs as gf

phone_general_re = re.compile(r'^(0047|\+47)?[0-9]\d{7}$', re.IGNORECASE) #First suggestion. Phone numbers were in different formats, so it was easily to just write a good audit function
phone_special_re = re.compile(r'^(\d{3}|\d{4}|\d{5}|\d{6})$')

def audit_phone(doubtful_phonenumbers, phone_number):
    if not phone_general_re.match(phone_number) and not phone_special_re.match(phone_number):
        gf.add_to_array(phone_number, doubtful_phonenumbers)

def audit(osmfile):
    doubtful_phones = []
    with open(osmfile, 'r') as xml_file:
        for event, elem in ET.iterparse(xml_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    k = tag.attrib['k'].encode('utf-8')
                    v = tag.attrib['v'].encode('utf-8')
                    if k == "phone":
                        audit_phone(doubtful_phones, v)
                    
    xml_file.close()
    print('\nProblem with data - phone numbers')
    pprint(doubtful_phones)

if __name__ == '__main__':
    audit(gf.OSM_FILE)
