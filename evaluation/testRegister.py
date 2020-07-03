import json
import requests
import time
import click


@click.command()
@click.option('--num_test', default=10, type=int, help="number of random tests, by default is 10")
def main(num_test):
    totalTime = 0
    for i in range (1, num_test+1):
        print (f"----test round {i} ----")

        totalTime += registerThing(f"TDBus{i}", "SingleDirectory")
    avgTime = float(totalTime) / num_test
    print (f"{num_test} files registered successfully, average time is {avgTime} s")
    return

def registerThing(tdFile, location, publicity=0):
    """
    read a TD from test file folder
    """

    url = 'http://localhost:4999/api/register'
    with open (f'TestFiles/{tdFile}.json', 'r', encoding='utf8') as fp:
        td = json.load(fp)

    payload = {
            "location": location,
            "td": td,
            "publicity": publicity
    }
    header = {
        'Content-Type': 'application/json', 
        'Accept-Charset': 'UTF-8'
    }
    start_time = time.time()
    response = requests.post(url, data=json.dumps(payload), headers=header)
    print (response.status_code, type(response.status_code))
    end_time = time.time()
    if (response.status_code != 200):
        raise Exception("The test operation failed, response code incorrect!")
    timespan = end_time-start_time
    print (f"This registration takes {timespan}")
    return timespan


if __name__ == "__main__":
    main()