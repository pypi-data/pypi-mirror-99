from os import EX_CANTCREAT
import pymongo
import urllib
from ChristisMongo.core.config_parser import get_mongo_configuration

def get_mongo_client(config_path):
    mongoConfiguration = get_mongo_configuration(config_path)
    if('ErrorCode' in mongoConfiguration):
        return mongoConfiguration
    username = urllib.parse.quote_plus(mongoConfiguration['mongo_user'])
    password = urllib.parse.quote_plus(mongoConfiguration['mongo_password'])
    serverAddress = mongoConfiguration['mongo_address']
    accessURL = "mongodb://{0}:{1}@{2}".format(username,password,serverAddress)
    client = pymongo.MongoClient(accessURL)
    # https://pymongo.readthedocs.io/en/stable/migrate-to-pymongo3.html#mongoclient-connects-asynchronously
    try:
        DBs = client.list_database_names()
    except pymongo.errors.ConnectionFailure as e:
        Error = {"ErrorCode":"700","ErrorMsg":e}
        return Error
    except pymongo.errors.ServerSelectionTimeoutError as e:
        Error = {"ErrorCode":"700","ErrorMsg":e}
        return Error
    except pymongo.errors.OperationFailure as e:
        Error = {"ErrorCode":"700","ErrorMsg":e}
        return Error
    except :
        Error = {"ErrorCode":"700","ErrorMsg":"Other Erros"}
    else:
        return client