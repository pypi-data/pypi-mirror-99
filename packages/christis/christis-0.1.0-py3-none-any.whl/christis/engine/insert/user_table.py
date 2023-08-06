import ChristisMongo.table.add as CM_add

def add_2_user_table(userList: list,group):
    userCandidateForStage = []
    for user in userList:
      result = CM_add.add_entry_one(database_name=group,table_name="user",data=user)
      if (type(result) == dict and 'ErrorCode' in result):
        if(result['ErrorCode'] != '701'):
            print("Error: MongoDB. Error Message: {0}".format(result['ErrorMsg']))
        continue
      userCandidateForStage.append(user['user_dn'])
    return userCandidateForStage

def add_2_pre_user_table(userList: list,group):
    pre_user = []
    for user in userList:
      result = CM_add.add_entry_one(database_name=group,table_name="pre_user",data=user)
      if (type(result) == dict and 'ErrorCode' in result):
        if(result['ErrorCode'] != '701'):
            print("Error: MongoDB. Error Message: {0}".format(result['ErrorMsg']))
        continue
      pre_user.append(user['user_dn'])
    return pre_user