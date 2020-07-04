import json
import requests
import time
import click


@click.command()
@click.option('--num_test_bus', default=100, type=int, help="number of bus file, by default is 100")
@click.option('--num_test_light', default=100, type=int, help="number of light file, by default is 100")
@click.option('--num_test_thermo', default=100, type=int, help="number of thermometer file, by default is 100")
@click.option('--num_test_random', default=100, type=int, help="number of random file, by default is 100")
def main(num_test_bus, num_test_light, num_test_thermo, num_test_random):
    totalTime = 0
    for i in range (1, num_test_bus+1):
        print (f"----test round {i} for bus----")
        totalTime += registerThing(f"TDBus{i}", "SingleDirectory")

    for i in range (1, num_test_light+1):
        print (f"----test round {i} for light----")
        totalTime += registerThing(f"TDLight{i}", "SingleDirectory")

    for i in range (1, num_test_thermo+1):
        print (f"----test round {i} for thermometer----")
        totalTime += registerThing(f"TDThermo{i}", "SingleDirectory")

    for i in range (1, num_test_random+1):
        print (f"----test round {i} for random file----")
        totalTime += registerThing(f"TDfile{i}", "SingleDirectory")

    avgTime = float(totalTime) / (num_test_bus + num_test_light + num_test_thermo + num_test_random)

    print (f"{num_test_bus} bus, {num_test_light} light, {num_test_thermo} thermometer, {num_test_random} random files registered successfully, average time is {avgTime} s")
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