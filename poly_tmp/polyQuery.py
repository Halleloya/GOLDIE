from pymongo import MongoClient, GEO2D

cl = MongoClient().poly.TD # db=poly collection=TD
cl.create_index([("properties.geo.coordinates", GEO2D)]) # GEO2D is the index method, don't have to apply

polygon = [[-75,40.7],[-75,40.8],[-73,40.8],[-73,40.7],[-75,40.7]] # Note five nodes are needed to represent a square


def geoWithin(polygon):
    '''
    input: a polygon 
    output: a cursor refered to a list of TDs, where all the TDs are inside the polygon
    '''
    results = cl.find({"properties.geo.coordinates":{"$geoWithin":{"$polygon": polygon}}})
    return results, results.count()


if __name__ == '__main__':
    a, b = geoWithin(polygon)
    print (a, b)
    '''
    for i in a:
        print (i)
    '''