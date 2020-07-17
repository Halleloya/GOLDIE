import json
import requests
import time
import click

"""
Three script query samples: 
number of buses running inside a polygon; 
average data of thermometers; 
number of lights that are on.
"""

@click.command()
@click.option('--num_test', default=3, type=int, help="number of random tests, by default is 1")
def main(num_test):
    totalTime = 0
    for i in range (1, num_test+1):
        print (f"----test round {i} ----")

        totalTime += cusQueryThing(f"scriptQuery{i}")
    avgTime = float(totalTime) / num_test
    print (f"{num_test} queries excuted successfully, average time is {avgTime} s")
    return

def cusQueryThing(tdFile):
    """
    Aggregation query TDs with customized script
    """

    url = 'http://localhost:5001/api/custom_query'
    with open (f'QueryScript/{tdFile}.json', 'r', encoding='utf8') as fp:
        queryScript = json.load(fp)
    print (queryScript, type(queryScript))
    params = {
            "data": json.dumps(queryScript)
    }
    header = {
        'Content-Type': 'application/json', 
        'Accept-Charset': 'UTF-8'
    }
    print (f"Querying with your customized script!")
    start_time = time.time()
    response = requests.get(url, params=params, headers=header)
    print (response.status_code, type(response.status_code))   
    end_time = time.time()
    print (response.text)
    if (response.status_code != 200):
        raise Exception("The test operation failed, response code incorrect!")
    timespan = end_time-start_time
    print (f"This query takes {timespan}")
    return timespan


if __name__ == "__main__":
    main()