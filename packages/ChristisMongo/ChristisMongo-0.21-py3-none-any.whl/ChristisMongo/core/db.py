from ChristisMongo.core.connection import get_mongo_client
from ChristisMongo.core.config_parser import get_mongo_configuration_path

#CHRISTIS_MONGO_CONFIG_FILE
mongoConfigPath = get_mongo_configuration_path()

def get_db(dbName):
    
    mongoClient = get_mongo_client(mongoConfigPath)
    if(type(mongoClient) == dict and 'ErrorCode' in mongoClient):
        return mongoClient
    dblist = mongoClient.list_database_names()
    if dbName in dblist:
        return mongoClient[dbName]
    else:
        return mongoClient[dbName]