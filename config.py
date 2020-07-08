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


class Level2DevConfig(DevConfig):
    HOST_NAME = "level2"
    ENV_NAME = "Level2-Dev"
    PORT=5002
    MONGODB_PORT = 27017
    MONGODB_DB = 'level2'
    MONGO_DBNAME = 'level2'
    MONGO_URI = "mongodb://localhost:27017/level2"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5002/'
    OAUTH2_JWT_KEY = 'level2-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level3DevConfig(DevConfig):
    HOST_NAME = "level3"
    ENV_NAME = "Level3-Dev"
    PORT=5003
    MONGODB_PORT = 27017
    MONGODB_DB = 'level3'
    MONGO_DBNAME = 'level3'
    MONGO_URI = "mongodb://localhost:27017/level3"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5003/'
    OAUTH2_JWT_KEY = 'level3-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level4aDevConfig(DevConfig):
    HOST_NAME = "level4a"
    ENV_NAME = "Level4a-Dev"
    PORT=5004
    MONGODB_PORT = 27017
    MONGODB_DB = 'level4a'
    MONGO_DBNAME = 'level4a'
    MONGO_URI = "mongodb://localhost:27017/level4a"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5004/'
    OAUTH2_JWT_KEY = 'level4a-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level4bDevConfig(DevConfig):
    HOST_NAME = "level4b"
    ENV_NAME = "Level4b-Dev"
    PORT=5005
    MONGODB_PORT = 27017
    MONGODB_DB = 'level4b'
    MONGO_DBNAME = 'level4b'
    MONGO_URI = "mongodb://localhost:27017/level4b"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5005/'
    OAUTH2_JWT_KEY = 'level4b-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level5aDevConfig(DevConfig):
    HOST_NAME = "level5a"
    ENV_NAME = "Level5a-Dev"
    PORT=5006
    MONGODB_PORT = 27017
    MONGODB_DB = 'level5a'
    MONGO_DBNAME = 'level5a'
    MONGO_URI = "mongodb://localhost:27017/level5a"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5006/'
    OAUTH2_JWT_KEY = 'level5a-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


class Level5bDevConfig(DevConfig):
    HOST_NAME = "level5b"
    ENV_NAME = "Level5b-Dev"
    PORT=5007
    MONGODB_PORT = 27017
    MONGODB_DB = 'level5b'
    MONGO_DBNAME = 'level5b'
    MONGO_URI = "mongodb://localhost:27017/level5b"
    # OAUth2
    OAUTH2_JWT_ENABLED = True
    OAUTH2_JWT_ISS = 'http://localhost:5007/'
    OAUTH2_JWT_KEY = 'level5b-secret'
    OAUTH2_JWT_ALG = 'HS256'
    OAUTH2_JWT_EXP = 3600


dev_config = {
    "level1": Level1DevConfig,
    "level2": Level2DevConfig,
    "level3": Level3DevConfig,
    "level4a": Level4aDevConfig,
    "level4b": Level4bDevConfig,
    "level5a": Level5aDevConfig,
    "level5b": Level5bDevConfig
}


class DepConfig(BaseConfig):
    # Deployment Environment Configurations
    ENV_NAME = "Deployment"
