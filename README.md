# Wrangle OpenStreetMap Data
Udacity Data Analyst Nanodegree

##Project Overview
The goal of this project is to choose any area of the world in https://www.openstreetmap.org, audit and clean dataset, coverting it from XML to JSON. 
Then import the cleaned .json file into a MongoDB database.
After that explore data by running queries.

##File description
[Postnummerregister_Excel.xlsx](Postnummerregister_Excel.xlsx): is a list of Norwegian postcodes. It's uses in project to compare postcodes and cities from dataset.
[Stavanger_Norway.osm](Stavanger_Norway.osm) : Choosed map area - Stavanger/Sandnes area, Norway
[Sample.osm](Sample.osm): My sample data wasn't generater by code from Project Details (Step Six - Document your Work). But by choosing smaller area (exactly Sandnes city) inside choosen area.
[global_funcs.py](global_funcs.py): contains functions which is used in multiply .py files
[clean_import.py](clean_import.py): cleans dataset, coverting it from XML to JSON and imports the cleaned .csv file to MongoDB database
[querying_data.py](querying_data.py): explores data by running queries

