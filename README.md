# Droit_v2

This repository contains implementation and utility code for Droit project, version 2. 

If you have any concerns or suggestions, please contact us at lyhao[AT]cs.columbia.edu. 

Major modification from the prior version: build a web app and implement federated identity management, abandon the access control mechanism in the previous version. We haven't find a concerete access control mechanism yet.

## Acknowledgement
We would like to thank Yifan for his valuable input and contribution on the implementation of this  prototype. 

## How to bootstrap the project

1. `git clone git@github.com:Halleloya/Droit_v2.git`.
2. Install dependencies `pip install -r requirements.txt`.
3. Configure the database, e.g., store your database in data/db, and `mongod --dbpath Droit/data/db`
4. Run the shell `python runall.py` or `./run.sh`. It create a simple tree-like structure illustrated in the following section. 

Sidenotes:

To run a local directory in the current structure `python run.py --level [level name]`. Try `python run.py --help` for more information. 

To run a single directory `python -m Droit.run`. It is easy and basically enough to test basic functions.

Please note that you are supposed to change the [ip] and [port] manually in the `config.py` file, if needed. 

## A sample walk-through 

Below we show a sample walk-through with a binary tree-like structure.

```
level1 (master)
level2a level2b
level3aa level3ab level3ba level3bb
level4aaa level4aab level4aba level4abb level4baa level4bab level4bba level4bbb  
level5aaaa level5aaab ...
level6aaaaa level6aaaab ...
```

## Settings

By default, all the directoires run on localhost. The tree-like structure starts from port 5001, with the name of level1 (also called master directory or root directory). The single directory module named SingleDirectory runs on port 4999.

MongoDB runs on its default port 27017. 

## Authentication

We utilize OpenID library to implement a federated identtiy assertion model among directories. In general, one directory can rely on its counterparts to authenticate a user after some configurations. From a user's perspective, one can sign in a directory with identity from another directory. 


http://localhost:5001/auth/oidc_auth_code/level2

change the providers_config with the client's id and secret 
