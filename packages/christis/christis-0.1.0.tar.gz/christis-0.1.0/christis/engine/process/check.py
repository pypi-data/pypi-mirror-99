import ChristisMongo.table.get as CM_get
import ChristisMongo.table.query as CM_query

# The method check users of User and PreUser table to find which user was deleted from LDAP
def check_ldap_deleted_user(k8group):

    users = CM_get.get_all_entries(database_name=k8group,table_name="user")
    candidateToDelete = []
    for user in users['Enteries']:
        result = CM_query.query_user_by_id(database_name=k8group,table_name='pre_user',id=user['_id'])
        if ('ErrorCode' in result):
            continue
        if(len(list(result['Enteries']))==0):
            candidateToDelete.append(user)
    return candidateToDelete


