# Droit_v2

This repository contains implementation and utility code for Droit project. Droit protects droit, so all rights reserved.

If you have any concerns or suggestions, please email lyhao[AT]cs.columbia.edu. 

Modification from version one: build a web app, abandon the access control mechanism in the previous version.

We would like to thank Yifan for his valuable input and contribution on the implementation of this  prototype. 

## How to bootstrap the project

1. `git clone git@github.com:Halleloya/Droit_v2.git`.
2. Install dependencies `pip install -r requirements.txt`.
3. Configure the database, e.g., store your database in data/db, and `mongod --dbpath data/db`
4. Run the shell `python runall.py`. 

Sidenotes:

To run a local directory `python -m Droit.run`

Please note that you are supposed to change the [ip] and [port] manually. 

## A sample walk-through 

Below we show a sample walk-through with the tree-like structure.

```
level1
level2a level2b
level3aa level3ab level3ba level3bb
level4aaa level4aab level4aba level4abb level4baa level4bab level4bba level4bbb  
level5aaaa level5aaab ...
level6aaaaa level6aaaab ...
```

### Utils

We also provide util programs for using the system.


## auth

http://localhost:5001/auth/oidc_auth_code/level2

change the providers_config with the client's id and secret 
