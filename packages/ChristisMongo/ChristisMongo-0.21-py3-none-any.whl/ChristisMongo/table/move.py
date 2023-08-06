from ChristisMongo.core import collection
import ChristisMongo.table.query as mquery
import ChristisMongo.table.delete as mdelete
import ChristisMongo.table.add as madd

def move_by_email(database_name,srcTable,dstTable,email):

    srcEntry = mquery.query_user_by_email(database_name,srcTable,email)
    user = {}
    for u in srcEntry['Enteries']:
        user = u
    result = madd.add_entry_one(database_name,dstTable,user)
    if (type(result) == dict and "ErrorCode" in result):
        return {"ErrorCode":"700","ErrorMsg":"Can't move , {0}".format(result['ErrorMsg'])}

    mdelete.delete_user_by_email(database_name,srcTable,email)

    return result

def move_by_cn(database_name,srcTable,dstTable,userCN):

    srcEntry = mquery.query_user_by_cn(database_name,srcTable,userCN)
    user = {}
    for u in srcEntry['Enteries']:
        user = u
    result = madd.add_entry_one(database_name,dstTable,user)
    if (type(result) == dict and "ErrorCode" in result):
        return {"ErrorCode":"700","ErrorMsg":"Can't move , {0}".format(result['ErrorMsg'])}

    mdelete.delete_user_by_cn(database_name,srcTable,userCN)

    return result

def move_by_dn(database_name,srcTable,dstTable,userDN):

    srcEntry = mquery.query_user_by_dn(database_name,srcTable,userDN)
    user = {}
    for u in srcEntry['Enteries']:
        user = u
    result = madd.add_entry_one(database_name,dstTable,user)
    if (type(result) == dict and "ErrorCode" in result):
        return {"ErrorCode":"700","ErrorMsg":"Can't move , {0}".format(result['ErrorMsg'])}

    mdelete.delete_user_by_dn(database_name,srcTable,userDN)

    return result

def move_by_id (database_name,srcTable,dstTable,userID):

    srcEntry = mquery.query_user_by_id(database_name,srcTable,userID)
    user = {}
    for u in srcEntry['Enteries']:
        user = u
    result = madd.add_entry_one(database_name,dstTable,user)
    if (type(result) == dict and "ErrorCode" in result):
        return {"ErrorCode":"700","ErrorMsg":"Can't move , {0}".format(result['ErrorMsg'])}

    mdelete.delete_user_by_id(database_name,srcTable,userID)

    return result