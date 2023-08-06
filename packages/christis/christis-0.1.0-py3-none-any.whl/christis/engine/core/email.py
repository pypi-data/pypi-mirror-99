import ChristisRequestor.group as CR_group
import ChristisRequestor.user as CR_user

def get_users_email(group):
    k8sGroup = group
    answerMsg = CR_group.get_group_members(groupCN=k8sGroup)
    if ('ErrorCode' in answerMsg):
        return answerMsg
    members = answerMsg['Response']
    membersEmail = {}
    for member in members:
       answerEmail = CR_user.get_user_email(userDN=member)
       if( type(answerEmail)==dict and 'ErrorCode' in answerEmail):
           membersEmail[member]="404"
           continue
       membersEmail[member]=answerEmail['Response']
    return membersEmail

def get_user_email_byDN(userDN):

    answerMsg = CR_user.get_user_email(userDN=userDN)

    if('ErrorCode' in answerMsg):
        return None
    email = answerMsg['Response']
    return email