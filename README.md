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


## auth

http://localhost:5001/auth/oidc_auth_code/level2

change the providers_config with the client's id and secret 
