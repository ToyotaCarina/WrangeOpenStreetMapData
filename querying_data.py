# -*- coding: utf-8 -*-
from pprint import pprint
import re
import global_funcs as gf

def unique_users_number(db):
    print '\nNumber of unique users'
    print len(db.stavanger.distinct('created.uid'))

def top10_contributing_users(db):
    document_number = db.stavanger.count()
    pipeline = [{"$group":{"_id":"$created.user" ,"count":{"$sum":1}}},
                {"$project":{"count":1,"percentage":{"$multiply":[{"$divide":[100,document_number]},"$count"]}}},
                { "$sort" : { "count" : -1}},
                {"$limit":10}
                ]
    stavanger_source('Top 10 contributing users:', db, pipeline)

def top10_most_referred_amenities(db):
    pipeline = [{"$match":{"amenity":{"$exists":1}}},
                {"$group":{"_id":"$amenity",
                "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":10}]
    stavanger_source('Top 10 most referred amenities:', db, pipeline)    

def nodes_ways_number(db):
    pipeline = [{"$match":{"type":{"$in":["node", "way"]}}},  
                {"$group":{"_id":"$type",
                        "count":{"$sum":1}}}
                ]
    stavanger_source('Number of nodes and ways:', db, pipeline)

def top5_cuisines(db):
    #if we remove '"cuisine": { "$exists" : 1}' we will actually see that many places doesn't have specified cuisine 
    pipeline = [{ "$match" : { "amenity" : { "$in" : ["restaurant", "fast_food", "cafe"] }, "cuisine": { "$exists" : 1}}},
                { "$group" : { "_id" : "$cuisine",
                            "count" : {"$sum" : 1}}},
                { "$sort" : { "count" : -1}},
                {"$limit":5}
                ]
    stavanger_source('Top 5 cuisines:', db, pipeline)

def kindergarten_and_school(db):
    print '\nNumbers of school facilities:'
    print 'Kindergartens: ' + str(db.stavanger.find({"amenity":"kindergarten"}).count())
    print 'Primary schools: ' + str(db.stavanger.find({"amenity":"school", "name" : {"$not" :re.compile("/.*videregående.*/", re.IGNORECASE)}}).count())
    print 'Secondary schools: ' + str(db.stavanger.find({"amenity":"school", "name" : {"$regex": ".*videregående.*", '$options' : 'i'} }).count())
    print 'Colleges: ' + str(db.stavanger.find({"amenity":"college"}).count())
    print 'Universities: ' + str(db.stavanger.find({"amenity":"university"}).count())

def most_referred_street_by_town(db):
    pipeline = [{"$match":{"address.city":{"$exists":1}}},
                {"$group":{"_id": {"city":"$address.city","street":"$address.street"},
                            "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$group":{"_id": "$_id.city",
                           "street":{"$first":"$_id.street"}}},
                {"$sort":{"_id":1}}]                                                
    stavanger_source('Most referred street, groupped by town:', db, pipeline)

def parking_investigation(db):
    print '\nInvestigating parking lots:'
    pipeline = [{"$match":{"amenity":"parking"}},
                {"$group":{"_id": "$access",
                            "count":{"$sum":1}}},
                {"$sort":{"count":-1}}]                                             
    stavanger_source('Parking access:', db, pipeline)

    pipeline = [{"$match":{"amenity":"parking"}},
                {"$group":{"_id": "$capacity",
                            "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":5}]                                             
    stavanger_source('Parking capacity:', db, pipeline) 
              

def stavanger_source(title, db, pipeline):
    print '\n' + title
    pprint([doc for doc in db.stavanger.aggregate(pipeline)])

def querying(db):
    nodes_ways_number(db)
    unique_users_number(db)
    top10_contributing_users(db)   
    top10_most_referred_amenities(db)
    kindergarten_and_school(db)
    top5_cuisines(db)
    most_referred_street_by_town(db)
    parking_investigation(db)

if __name__ == '__main__':    
    db = gf.MongoDB_connect()
    querying(db) 
