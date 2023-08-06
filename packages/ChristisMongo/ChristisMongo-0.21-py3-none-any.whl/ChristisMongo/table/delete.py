from ChristisMongo.core import collection

def delete_abstract_one(database_name,table_name,query):

    table = collection.get_collection(database_name,table_name)
    if(type(table) == dict and 'ErrorCode' in table):
        return table
    try:
        result = table.delete_one(query)
    except Exception as e:
        return {"ErrorCode":"700","ErrorMsg":e}
    else:
        return {"StatusCode":"200","Response":result}

def delete_abstract_multiple(database_name,table_name,query):

    table = collection.get_collection(database_name,table_name)
    if(type(table) == dict and 'ErrorCode' in table):
        return table
    try:
        result = table.delete_many(query)
    except Exception as e:
        return {"ErrorCode":"700","ErrorMsg":e}
    else:
        return {"StatusCode":"200","Response":result}


def delete_user_by_email(database_name,table_name,email):

    emailQuery = {"email":str(email)}

    result = delete_abstract_one(database_name,table_name,emailQuery)
    return result

def delete_user_by_cn(database_name,table_name,cn):

    cnQuery = {"user_cn":str(cn)}

    result = delete_abstract_one(database_name,table_name,cnQuery)
    return result

def delete_user_by_dn (database_name,table_name,dn):

    dnQuery = {"user_dn":str(dn)}

    result = delete_abstract_one(database_name,table_name,dnQuery)
    return result

def delete_user_by_role(database_name,table_name,role):

    roleQuery = {"role":str(role)}

    result = delete_abstract_multiple(database_name,table_name,roleQuery)
    return result

def delete_user_by_id(database_name,table_name,id):

    idQuery = {"_id":id}

    result = delete_abstract_one(database_name,table_name,idQuery)
    return result

# these two methods are used only for ROLE table
def delete_role_by_roleName(database_name,table_name,role):

    roleQuery = {"role_name":str(role)}

    result = delete_abstract_multiple(database_name,table_name,roleQuery)
    return result

def delete_role_by_roleID(database_name,table_name,roleID):

    roleIdQuery= {"_id":roleID}

    result = delete_abstract_one(database_name,table_name,roleIdQuery)
    return result

def delete_role_by_roleVersion(database_name,table_name,version):

    roleVersion= {"_id":version}

    result = delete_abstract_one(database_name,table_name,roleVersion)
    return result