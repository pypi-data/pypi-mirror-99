from ChristisMongo.core import collection

def query_abstract(database_name,table_name,query):

    table = collection.get_collection(database_name,table_name)
    if(type(table) == dict and 'ErrorCode' in table):
        return table
    try:
        entries = table.find(query)
    except Exception as e:
        return {"ErrorCode":"700","ErrorMsg":e}
    else:
        return {"StatusCode":"200","Enteries":entries}


def query_user_by_email(database_name,table_name,email):

    emailQuery = {"email":str(email)}

    entries = query_abstract(database_name,table_name,emailQuery)
    return entries

def query_user_by_cn(database_name,table_name,cn):

    cnQuery = {"user_cn":str(cn)}

    entries = query_abstract(database_name,table_name,cnQuery)
    return entries

def query_user_by_dn (database_name,table_name,dn):

    dnQuery = {"user_dn":str(dn)}

    entries = query_abstract(database_name,table_name,dnQuery)
    return entries

def query_user_by_role(database_name,table_name,role):

    roleQuery = {"role":str(role)}

    enteries = query_abstract(database_name,table_name,roleQuery)
    return enteries

def query_user_by_id(database_name,table_name,id):

    idQuery = {"_id":id}

    enteries = query_abstract(database_name,table_name,idQuery)
    return enteries

#  these two methods are used only for ROLE table
def query_role_by_roleName(database_name,table_name,role):

    roleQuery = {"role_name":str(role)}

    enteries = query_abstract(database_name,table_name,roleQuery)
    return enteries

def query_role_by_roleID(database_name,table_name,roleID):

    idQuery = {"_id":roleID}

    enteries = query_abstract(database_name,table_name,idQuery)
    return enteries

def query_role_by_roleVersion(database_name,table_name,version):

    roleQuery = {"version":version }

    enteries = query_abstract(database_name,table_name,roleQuery)
    return enteries