import yaml
import os
import sys

def get_mongo_configuration(configPath):
    if os.path.exists(configPath):
        try:
            with open(configPath) as file:
                mongoConfiguartion = {}
                mongoConfiguartion = yaml.load(file, Loader=yaml.FullLoader)
        except IOError as e:
            Error = {"ErrorCode":"505","ErrorMsg":"I/O error({0}): {1}".format(e.errno, e.strerror)}
        except:
            Error = {"ErrorCode":"505","ErrorMsg":sys.exc_info()[1]}
            return Error
        else:       
            return mongoConfiguartion['MongoDB']
    else:
        Error = {"ErrorCode":"404","ErrorMsg":"Config File not found"}
        return Error

def get_mongo_configuration_path():
    Home = os.environ['HOME']
    return "{0}/.christisCLI/mongo.yaml".format(Home)