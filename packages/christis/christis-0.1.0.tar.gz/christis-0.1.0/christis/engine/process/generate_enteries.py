from christis.engine.core.cn import *
from christis.engine.core.email import get_user_email_byDN
from christis.engine.core.general import get_sha2

def get_user_table_enteries(emails: dict , hashEmails: dict):

    data = []

    for userdn,email in emails.items():
        entry = {}
        entry["email"]= email
        entry["user_dn"] = userdn
        data.append(entry)
    
    for e in data:
        e['_id'] = hashEmails[e['user_dn']]
    
    return data

def get_stage_table_enteries(stageCandidateList: list):

    stageUserList = []
    
    for user in stageCandidateList:
        stageCandidate = {}
        email = get_user_email_byDN(user)
        stageCandidate['_id'] = get_sha2(email)
        stageCandidate['email'] = email
        stageCandidate['user_cn'] = get_user_cn(user)
        stageCandidate['user_dn'] = user
        stageUserList.append(stageCandidate)
    
    return stageUserList
        
    
