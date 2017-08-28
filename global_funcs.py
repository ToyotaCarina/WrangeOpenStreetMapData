import xlrd
import math
import os
from pymongo import MongoClient

sample_file = 'Sample.osm'
whole_file = 'Stavanger_Norway.osm'
OSM_FILE = whole_file
JSON_FILE = "{0}.json".format(OSM_FILE)
norwegian_postcodes_file = 'Postnummerregister_Excel.xlsx' #uses to check postcodes in dataset

def add_to_dict(key,dictionary):
    if key not in dictionary.keys():
        dictionary[key] = 1
    else:
        dictionary[key] += 1

def add_to_array(val, array):
    if val not in array:
        array.append(val)

def print_file_sizes(filenames):
    print('\nFile sizes:')
    for filename in filenames:
        print(filename + ': ' + convert_size(os.path.getsize(filename)))    

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def parse_postcodes_file():
    postcodes_dict = {}
    workbook = xlrd.open_workbook(norwegian_postcodes_file)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(r, col)
                for col in range(2)] 
                    for r in range(sheet.nrows)]
    postcodes_dict = dict((key, value.lower()) for (key, value) in data)    
    return postcodes_dict

def MongoDB_connect():
    client = MongoClient("mongodb://localhost:27017")
    db = client.OpenStreetMap
    return db

def MongoDB_insert_data(data, db):
    # cleaning table to avoid duplicate inserting
    db.stavanger.remove() 
    db.stavanger.insert(data)
