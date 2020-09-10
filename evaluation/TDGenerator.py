'''
This program generates testing files

Date: Feb. 2020
'''
import random
import string
import json
import os
import click

propertyList = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
actionList = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
eventList = ["This is event 1", "This is event 2", "This is event 3",
             "This is event 4"]  # Event is not important for the test purpose

@click.command()
@click.option('--num_file', default=100, type=int, help="number of random test files, by default is 10")
@click.option('--num_light', default=100, type=int, help="number of random test files, by default is 10")
@click.option('--num_thermo', default=100, type=int, help="number of random test files, by default is 10")
@click.option('--num_bus', default=1000, type=int, help="number of random test files, by default is 10")
def main(num_file, num_light, num_thermo, num_bus):
    """
    Generate the test TD files
    """
    cnt_file = cnt_light = cnt_thermo = cnt_bus = 1
    while cnt_file <= num_file: # NUMBER_OF_FILE:
        td = generateOnto(cnt_file)
        fname = "TDfile" + str(cnt_file) + ".json"
        generateFile(td)
        writeFile(fname, td)
        cnt_file += 1
    while cnt_light <= num_light: # NUMBER_OF_LIGHT:
        td = generateOnto(cnt_light + num_file)
        fname = "TDLight" + str(cnt_light) + ".json"
        generateLight(td)
        writeFile(fname, td)
        cnt_light += 1
    while cnt_thermo <= num_thermo: # NUMBER_OF_THERMOMETER:
        td = generateOnto(cnt_thermo + num_file + num_light)
        fname = "TDThermo" + str(cnt_thermo) + ".json"
        generateThermo(td)
        writeFile(fname, td)
        cnt_thermo += 1
    while cnt_bus <= num_bus: # NUMBER_OF_BUS:
        td = generateOnto(cnt_bus + num_file + num_light + num_thermo)
        fname = "TDBus" + str(cnt_bus) + ".json"
        generateBus(td)
        writeFile(fname, td)
        cnt_bus += 1

    return


def writeFile(fname, td):
    dir_name = "TestFiles"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    fw = open(os.path.join(dir_name, fname), 'w', encoding='utf-8')
    json.dump(td, fw, ensure_ascii=False, indent=4)
    fw.close()

    print(fname + ' DONE!')
    return


def generateLight(td):
    td["@type"] = "light"
    td["properties"]["status"] = {"data": random.randint(0, 1), "description": "on or off", "forms": [
        {"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}
    #td["properties"]["location"] = {"loc": "%s" % random.choice(location), "forms": [{"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["actions"]["action%d" % i] = {"description": random.choice(actionList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["invokeaction"]}], "safe": False, "idempotent": False}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["events"]["event%d" % i] = {"description": random.choice(eventList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["subscribeevent"]}]}

    return


def generateThermo(td):
    td["@type"] = "thermometer"
    td["properties"]["temperature"] = {"data": round(random.uniform(0, 86), 2), "description": "temperature degree", "forms": [
        {"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}
    #td["properties"]["location"] = {"loc": "%s" % random.choice(location), "forms": [{"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["actions"]["action%d" % i] = {"description": random.choice(actionList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["invokeaction"]}], "safe": False, "idempotent": False}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["events"]["event%d" % i] = {"description": random.choice(eventList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["subscribeevent"]}]}

    return


def generateBus(td):
    td["@type"] = "bus"
    td["properties"]["status"] = {"description": "running or not? not important", "forms": [
        {"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}
    #td["properties"]["location"] = {"loc": "%s" % random.choice(location), "forms": [{"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    td["properties"]["geo"] = {"coordinates": [round(random.uniform(-73.83, -74.1), 5), round(random.uniform(
        40.7, 40.9), 5)], "forms": [{"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["actions"]["action%d" % i] = {"description": random.choice(actionList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["invokeaction"]}], "safe": False, "idempotent": False}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["events"]["event%d" % i] = {"description": random.choice(eventList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["subscribeevent"]}]}

    return


def generateFile(td):
    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["properties"]["property%d" % i] = {"description": random.choice(propertyList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    #td["properties"]["location"] = {"loc": "%s" % random.choice(location), "forms": [{"href": "http:www.a.a", "contentType": "application/json", "op": ["readproperty"]}]}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["actions"]["action%d" % i] = {"description": random.choice(actionList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["invokeaction"]}], "safe": False, "idempotent": False}

    j = random.randint(1, 5)
    for i in range(1, j+1):
        td["events"]["event%d" % i] = {"description": random.choice(eventList), "forms": [
            {"href": "http:www.a.a", "contentType": "application/json", "op": ["subscribeevent"]}]}

    #td["location"] = "%s" % random.choice(location)

    return td


def generateOnto(tdid):
    td = {}
    td["@context"] = "https://www.w3.org/2019/wot/td/v1"
    # ran_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    td["id"] = f"urn:dev:wot:com:example:servient:{tdid}" # "urn:dev:wot:com:example:servient:%s" % ran_id
    ran_name = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    td["title"] = "%s" % ran_name
    td["@type"] = "thing"
    td["securityDefinitions"] = {"basic_sc": {
        "scheme": "basic", "in": "header"}, "nosec_sc": {"scheme": "nosec"}}
    td["security"] = ["nosec_sc"]

    td["properties"] = {}
    td["actions"] = {}
    td["events"] = {}

    return td


if __name__ == '__main__':
    main()
