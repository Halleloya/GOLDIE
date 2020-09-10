import json
import requests
import time
import click
import random

'''
Test 1
Test the time to register TDs with publicity=0,1,2...

'''


directory_names = ['SingleDirectory'] # ['level1', 'level2a', 'level2b', 'level3aa', 'level3ab', 'level4aba', 'level4abb', 'level5abba', 'level5abbb']
# ports = {'level1':5001, 'level2a':5002, 'level2b':5003, 'level3aa':5004, 'level3ab':5005, 'level4aba':5006, 'level4abb':5007, 'level5abba':5008, 'level5abbb':5009}


@click.command()
@click.option('--num_test_bus', default=200, type=int, help="number of bus file, by default is 100")
@click.option('--num_test_light', default=200, type=int, help="number of light file, by default is 100")
@click.option('--num_test_thermo', default=200, type=int, help="number of thermometer file, by default is 100")
@click.option('--num_test_random', default=200, type=int, help="number of random file, by default is 100")
def main(num_test_bus, num_test_light, num_test_thermo, num_test_random):
    totalTime = 0
    for i in range (1, num_test_bus+1):
        print (f"----test round {i} for bus----")
        location = random.choice(directory_names)
        totalTime += registerThing(f"TDBus{i}", location)

    for i in range (1, num_test_light+1):
        print (f"----test round {i} for light----")
        location = random.choice(directory_names)
        totalTime += registerThing(f"TDLight{i}", location)

    for i in range (1, num_test_thermo+1):
        print (f"----test round {i} for thermometer----")
        location = random.choice(directory_names)
        totalTime += registerThing(f"TDThermo{i}", location)

    for i in range (1, num_test_random+1):
        print (f"----test round {i} for random file----")
        location = random.choice(directory_names)
        totalTime += registerThing(f"TDfile{i}", location)

    avgTime = float(totalTime) / (num_test_bus + num_test_light + num_test_thermo + num_test_random)

    print (f"{num_test_bus} bus, {num_test_light} light, {num_test_thermo} thermometer, {num_test_random} random files registered successfully, average time is {avgTime} s")
    return

def registerThing(tdFile, location, publicity=0):
    """
    read a TD from test file folder
    """
    # port = ports[location]
    url = f'http://localhost:4999/api/register'
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
    end_time = time.time()
    print (response.status_code, type(response.status_code))   
    if (response.status_code != 200):
        raise Exception("The test operation failed, response code incorrect!")
    timespan = end_time-start_time
    print (f"This registration takes {timespan}")
    return timespan


if __name__ == "__main__":
    main()
