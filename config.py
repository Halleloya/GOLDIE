import os

"""
Set up the configuration for flask environment using classes

:BaseConfig: the parent class for all configuration class, used for common settings

:TestConfig: the configuration class for test environment
:DevConfig: the configuration class for development environment
:DepConfig: the configuration class for deployment environment
"""


class BaseConfig(object):
    # Used for flask session to generate session id
    SECRET_KEY = os.urandom(128)

    @classmethod
    def to_dict(cls):
        """
        Convert attributes to a dictionary form, which is used for Eve library setting
        """
        return {attr: getattr(cls, attr) for attr in dir(cls) if attr.isupper()}


class TestConfig(BaseConfig):
    # Testing Environment Configuration
    ENV_NAME = "Test"


"""
Development configurations
"""
class DevConfig(BaseConfig):
    # Development Environment Configuration
    ENV_NAME = "Development"
    # Mongo Engine
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

class Level1DevConfig(DevConfig):
    HOST_NAME = "level1"
    ENV_NAME = "Level1-Dev"
    PORT=5001
    # mongo engine
    MONGODB_PORT = 27017
    MONGODB_DB = 'level1'
    # pymongo
    MONGO_URI = "mongodb://localhost:27017/level1"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5001/'
    OAUTH2_JWT_KEY = 'level1-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level2aDevConfig(DevConfig):
    HOST_NAME = "level2a"
    ENV_NAME = "Level2a-Dev"
    PORT=5002
    MONGODB_PORT = 27017
    MONGODB_DB = 'level2a'
    MONGO_DBNAME = 'level2a'
    MONGO_URI = "mongodb://localhost:27017/level2a"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5002/'
    OAUTH2_JWT_KEY = 'level2a-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

class Level2bDevConfig(DevConfig):
    HOST_NAME = "level2b"
    ENV_NAME = "Level2b-Dev"
    PORT=5003
    MONGODB_PORT = 27017
    MONGODB_DB = 'level2b'
    MONGO_DBNAME = 'level2b'
    MONGO_URI = "mongodb://localhost:27017/level2b"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5003/'
    OAUTH2_JWT_KEY = 'level2b-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

class Level3aaDevConfig(DevConfig):
    HOST_NAME = "level3aa"
    ENV_NAME = "Level3aa-Dev"
    PORT=5004
    MONGODB_PORT = 27017
    MONGODB_DB = 'level3aa'
    MONGO_DBNAME = 'level3aa'
    MONGO_URI = "mongodb://localhost:27017/level3aa"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5004/'
    OAUTH2_JWT_KEY = 'level3aa-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

class Level3abDevConfig(DevConfig):
    HOST_NAME = "level3ab"
    ENV_NAME = "Level3ab-Dev"
    PORT=5005
    MONGODB_PORT = 27017
    MONGODB_DB = 'level3ab'
    MONGO_DBNAME = 'level3ab'
    MONGO_URI = "mongodb://localhost:27017/level3ab"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5005/'
    OAUTH2_JWT_KEY = 'level3ab-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

class Level4abaDevConfig(DevConfig):
    HOST_NAME = "level4aba"
    ENV_NAME = "Level4aba-Dev"
    PORT=5006
    MONGODB_PORT = 27017
    MONGODB_DB = 'level4aba'
    MONGO_DBNAME = 'level4aba'
    MONGO_URI = "mongodb://localhost:27017/level4aba"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5006/'
    OAUTH2_JWT_KEY = 'level4aba-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600

class Level4abbDevConfig(DevConfig):
    HOST_NAME = "level4abb"
    ENV_NAME = "Level4abb-Dev"
    PORT=5007
    MONGODB_PORT = 27017
    MONGODB_DB = 'level4abb'
    MONGO_DBNAME = 'level4abb'
    MONGO_URI = "mongodb://localhost:27017/level4abb"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5007/'
    OAUTH2_JWT_KEY = 'level4abb-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level5abbaDevConfig(DevConfig):
    HOST_NAME = "level5abba"
    ENV_NAME = "Level5abba-Dev"
    PORT=5008
    MONGODB_PORT = 27017
    MONGODB_DB = 'level5abba'
    MONGO_DBNAME = 'level5abba'
    MONGO_URI = "mongodb://localhost:27017/level5abba"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5008/'
    OAUTH2_JWT_KEY = 'level5abba-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level5abbbDevConfig(DevConfig):
    HOST_NAME = "level5abbb"
    ENV_NAME = "Level5abbb-Dev"
    PORT=5009
    MONGODB_PORT = 27017
    MONGODB_DB = 'level5abbb'
    MONGO_DBNAME = 'level5abbb'
    MONGO_URI = "mongodb://localhost:27017/level5abbb"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5007/'
    OAUTH2_JWT_KEY = 'level5abbb-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


dev_config = {
    "level1": Level1DevConfig,
    "level2a": Level2aDevConfig,
    "level2b": Level2bDevConfig,
    "level3aa": Level3aaDevConfig,
    "level3ab": Level3abDevConfig,
    "level4aba": Level4abaDevConfig,
    "level4abb": Level4abbDevConfig,
    "level5abba": Level5abbaDevConfig,
    "level5abbb": Level5abbbDevConfig
}


class DepConfig(BaseConfig):
    # Deployment Environment Configurations
    ENV_NAME = "Deployment"
