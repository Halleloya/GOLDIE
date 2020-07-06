# Droit_v2

This repository contains implementation and utility code for Droit project. Droit protects droit, so all rights reserved.

If you have any concerns or suggestions, please email lyhao[AT]cs.columbia.edu. 

Modification from version one: build a web app, abandon the access control mechanism in the previous version.

We would like to thank Yifan for his valuable input and contribution on the implementation of this  prototype. 

## How to bootstrap the project

1. `git clone git@github.com:Halleloya/Droit_v2.git`.
2. Install dependencies `pip install -r requirements.txt`.
3. Configure the database, e.g., store your database in data/db, and `mongod --dbpath data/db`
4. Run the shell. 

Sidenotes:

To run a local directory `python -m Droit.run`

To initialize database and start the application server as one go, use `./setup.sh` in `/Droit/src` (applied to a single server).

To initialize database at an application server, use `python3 -m Droit.level1.init_db`.

To initialize database at access-control server, use `python3 -m Droit.access.init_db`.

Please note that you are supposed to change the [ip] and [port] manually. 

## A simple walk-through (by default)

```
    0(1) 
    |
    1(2)
    | 
    0(3)
  /   \
1(4)   1(4b)
|      |
0(5)   0(5b)
```

0: nuc6
1: nuc7

### Utils

We also provide util programs for using the system.

You can use `bash ./Droit/evaluation/init_master` and `bash ./Droit/evaluation/init_secondary` to initiate the application nodes on `nuc6` and `nuc7` respectively, which are two physical machines we used to deploy our system.


### Without access control

> Registers a private TV at level5 (e.g. campus server)

`curl http://192.168.16.79:5000/register -X POST -d '{"targetLoc":"level5", "td":{"_type": "tv", "id": "urn:dev:ops:77777-tv-0001"}}' -H "Content-Type:application/json"`

> Registers a publc train at level5b (e.g. mta server), sets its publicity to be 1

`curl http://192.168.16.79:5001/register -X POST -d '{"targetLoc":"level5b", "td":{"_type": "train", "publicity": 1, "id": "urn:dev:ops:77777-train-0001"}}' -H "Content-Type:application/json"`

> Searches this TV with its location and type

`curl "http://192.168.16.79:5000/searchByLocType?loc=level5&type=tv"`

> Searches the TV with its loccation and ID

`curl "http://192.168.16.79:5000/searchByLocId?loc=level5&id=urn:dev:ops:77777-tv-0001"`

> Searches the the public train at level 2 (none) and 4b (the train registered). Note that by default, the item registered is private (publicity=0 and only expose to the registered directory).

`curl "http://192.168.16.79:5000/searchPublic?loc=level2"`

`curl "http://192.168.16.79:5000/searchPublic?loc=level4"`

> Relocates the TV from level5 to level5b

`curl -X PUT "http://192.168.16.79:5000/relocate?fromLoc=level5&toLoc=level5b&id=urn:dev:ops:77777-tv-0001"`

> Search tv at level5, no tv anymore; search tv at level5b, find the tv

`curl "http://192.168.16.79:5000/searchByLocType?loc=level5&type=tv"`
`curl "http://192.168.16.79:5000/searchByLocType?loc=level5b&type=tv"`

> Delete tv from level5b

`curl -X DELETE "http://192.168.16.79:5000/delete?targetLoc=level5b&id=urn:dev:ops:77777-tv-0001"`
