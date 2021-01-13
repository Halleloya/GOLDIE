# GOLDIE


This repository contains implementation and utility code for Droit project, version 2. 

If you have any concerns or suggestions, please contact us at lyhao[AT]cs.columbia.edu. 

Please cite the following paper if the project contributes to your work.
```
Luoyao Hao and Henning Schulzrinne, "GOLDIE: Harmonization and Orchestration Towards a Global Directory for IoT", IEEE International Conference on Computer Communications (INFOCOM), 2021.
```

## History

This repository used to be named as "Droit_v2". It is changed to "GOLDIE" in accordance with the name in our paper. Therefore, the term "Droit" may appear in the source codes anyway.  

As you can guess, there was a more sketchy and initial version named "Droit". Altough it shares basic insights of GOLDIE, it has been abandoned given some design flaws. Major modifications from that are: we build a web app and implement federated user identity management, however, the access control mechanism has been dropped off. Droit used a capability-based approach for access control with the help of JWT. Given the chanllenges in widely recognizing (i.e., forcing such a model is not very possible) and management (i.e., revoking delegated capabilities is knotty) through that approach, we want to leave it blank at this point (or leave it to each administration actually in GOLDIE).

By the way, we haven't find a concerete access control mechanism in the proposed scenario yet. We are working on it, and hopefully a potential solution will be illustrated in a relevant paper in the near future. 


## To bootstrap the project

1. `git clone git@github.com:Halleloya/Droit_v2.git`.
2. Install dependencies `pip install -r requirements.txt`.
3. Configure the database, e.g., store your database in data/db, and `mongod --dbpath Droit/data/db`
4. Run the shell `python runall.py` or `./run.sh`. It create a simple tree-like structure illustrated in the following section. 

Sidenotes:

To run a local directory in the current structure `python run.py --level [level name]`. Try `python run.py --help` for more information. 

To run a single directory `python -m Droit.run`. It is easy and basically enough to test basic functions.

Please note that you are supposed to change the [ip] and [port] manually in the `config.py` file, if needed. 

To disable InsecureTransportError of OAuth2 (as https is required, but run with http in localhost): add `export OAUTHLIB_INSECURE_TRANSPORT=1` to your env/bin/activate, or just input this command everytime restart the virtual environment. Please be noted that you should never do that in your production. 

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

MongoDB runs on its default port 27017. To run MongoDB on another port: add `--port [port]` when starting the database, and change the configure files to direct apps to database. 

To release all the ports occupied by directories: `sudo kill -9 $(lsof -i:5001 -i:5002 -i:5003 -i:5004 -i:5005 -i:5006 -i:5007 -i:5008 -t)`.

## Authentication

We utilize OpenID library to implement a federated identtiy assertion model among directories. In general, one directory can rely on its counterparts to authenticate a user after some configurations. From a user's perspective, one can sign in a directory with the identity from another directory. 

### Example 
To illustrate how to configure it, we give an example that level3aa provides a means of login with identity of level2b. In this example, level2b is the OIDC provider, while level3aa is the OIDC client.

> In level2b (http://localhost:5003/auth/oauth_list), register a new client. The only nonintuitive field is "Redirect URI", which is the address that the provider should redirect back to the client. In the example, it should be `http://localhost:5004/auth/oidc_auth_code/level2b`.

> In level3aa's backend configuration (Droit/auth/providers_config.py), change the providers_config with the client's id and secret specified in the known OIDC clients of level2b.

```
"level3aa": {
        "level2b": {
            "client_id": 'sQDK1uX1R62sZf3f9AB0eTJb',
            "client_secret": 'pkcqeqvYvzKE1zHjhRv30MFVcIDve6b4tZRmmjGf68M0ZmoK',
            "access_token_url": 'http://localhost:5003/auth/oidc_token',
            "access_token_params": None,
            "authorize_url": 'http://localhost:5003/auth/oidc_authorize',
            "authorize_params": None,
            "api_base_url": 'http://localhost:5003/api',
            "client_kwargs": {
                'scope': 'openid profile',
                'token_endpoint_auth_method': 'client_secret_basic'}
        }
    }
```

> Now you can login level3aa with your username and password in level2b.

## Acknowledgement
We would like to thank Yifan for his valuable input and contribution on the implementation of this  prototype. 

