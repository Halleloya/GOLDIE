import json
import requests
import time
import click


@click.command()
@click.option('--num_test', default=10, type=int, help="number of random tests, by default is 10")
@click.option('--location', default="level1", type=str, help="directory name you want to search, default is SingleDirectory")
@click.option('--thing_type', default=None, type=str, help="type of TD you want to search, default is None")
@click.option('--thing_id', default=None, type=str, help="id of TD you want to search, default is None")
def main(num_test, location, thing_type, thing_id):
    totalTime = 0
    for i in range (1, num_test+1):
        print (f"----test round {i} ----")

        totalTime += queryThing(location , thing_type, thing_id)
    avgTime = float(totalTime) / num_test
    print (f"{num_test} queries excuted successfully, average time is {avgTime} s")
    return

def queryThing(location, thing_type, thing_id):
    """
    query TDs with designated location, type, id
    """

    url = 'http://localhost:5001/api/search'

    params = {
            "location": location,
            "thing_type": thing_type,
            "thing_id": thing_id
    }
    header = {
        'Content-Type': 'application/json', 
        'Accept-Charset': 'UTF-8'
    }
    print (f"Querying {location}, with type = {thing_type}, id = {thing_id}")
    start_time = time.time()
    response = requests.get(url, params=params, headers=header)
    #print (response.status_code, type(response.status_code))   
    end_time = time.time()
    #print (response.text)
    if (response.status_code != 200):
        raise Exception("The test operation failed, response code incorrect!")
    timespan = end_time-start_time
    print (f"This query takes {timespan}")
    return timespan


if __name__ == "__main__":
    main()
