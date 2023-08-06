import ChristisRequestor.group as CR_group
import ChristisRequestor.user as CR_user

def get_user_cn(userDN):

    answerMsg = CR_user.get_user_cn(userDN=userDN)
    if ('ErrorCode' in answerMsg):
        return None
    cn = answerMsg['Response']
    return cn
