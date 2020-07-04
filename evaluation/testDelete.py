import json
import requests
import time
import click

thingIDs = ["urn:dev:wot:com:example:servient:QM3hYyAF", "urn:dev:wot:com:example:servient:PumwJSAE", "urn:dev:wot:com:example:servient:fqxEBLt0"]

@click.command()
@click.option('--num_test', default=3, type=int, help="number of random tests, by default is 10")
@click.option('--location', default="SingleDirectory", type=str, help="directory name you want to search, default is SingleDirectory")
@click.option('--thing_id', default=None, type=str, help="id of TD you want to search, default is None")
def main(num_test, location, thing_id):
    totalTime = 0
    for i in range (num_test):
        print (f"----test round {i+1} ----")
        thing_id = thingIDs[i]
        totalTime += deleteThing(location, thing_id)
    avgTime = float(totalTime) / num_test
    print (f"{num_test} delete operations excuted successfully, average time is {avgTime} s")
    return

def deleteThing(location, thing_id):
    """
    delete TDs with designated location, id
    """

    url = 'http://localhost:4999/api/delete'

    params = {
            "location": location,
            "thing_id": thing_id
    }
    header = {
        'Content-Type': 'application/json', 
        'Accept-Charset': 'UTF-8'
    }
    print (f"Deleting {location}, id = {thing_id}")
    start_time = time.time()
    response = requests.delete(url, params=params, headers=header)
    #print (response.status_code, type(response.status_code))   
    end_time = time.time()
    print (response.text)
    if (response.status_code != 200):
        raise Exception("The test operation failed, response code incorrect!")
    timespan = end_time-start_time
    print (f"This deletion takes {timespan}")
    return timespan


if __name__ == "__main__":
    main()