import typer
import os
from christis.engine.core.email import *
from christis.engine.core.general import *
from christis.engine.process.generate_enteries import *
from christis.engine.insert.user_table import *
from ChristisMongo.core.collection import get_collection
from ChristisMongo.table.add import *
import ChristisMongo.table.query as CM_query 
import ChristisMongo.table.delete as CM_delete
from christis.engine.process.check import check_ldap_deleted_user
import christis.cmd_database.view as view

app = typer.Typer()

app.add_typer(view.app,name="view",help="Commands for viewing tables like stage,main,...")

@app.command()
def sync():

    """
    Sync users from K8sGroup in your Active Directory to your Christis Database
    """

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']
    userEmails = get_users_email(k8sGroup)
    finalUserEmail = {}
    for user,email in userEmails.items():
        if (email=='404'):
            typer.echo("Error! The Email is not set for user: {0}. The user will be removed from update state!".format(user),err=True)
            continue
        finalUserEmail[user]=email
    
    emailsHash = {}
    for user,email in finalUserEmail.items():
        emailsHash[user] = get_sha2(email)
    # These users can be added to pre_user , user and stage
    userTableList = get_user_table_enteries(emails=finalUserEmail,hashEmails=emailsHash)

    # These list will be used to check user deletion
    preUserList = add_2_pre_user_table(userList=userTableList,group=k8sGroup)

    # Add these users to the user table , if the use can be added to user table it can be added to stage too!
    userCandidateForStage = add_2_user_table(userList=userTableList,group=k8sGroup)

    # These users should be deleted from stage,main,user because they are remove from K8s group in LDAP
    userCandidateToDelete = check_ldap_deleted_user(k8group=k8sGroup)

    if(len(userCandidateToDelete)>0):
        typer.echo("The roles and resources of following users will be deleted : ")
        i = 1
        for deletedUser in userCandidateToDelete:
            deletedUserEmail = deletedUser['email']
            typer.echo("User {0} >>>  Email : {1} | DN : {2} ".format(i,deletedUserEmail,deletedUser['user_dn']))
            i = i + 1
        # TODO Send Delete Operatin!!!! 
        # TODO : Should be deleted form User table and stage(if it exists on it) and from main!
        # The user first will be moved to the isolated users table and then it will be deleted form stage and user table
            answerMsg = CM_query.query_user_by_email(database_name=k8sGroup,table_name='stage',email=deletedUserEmail)

            if('ErrorCode' in answerMsg):
                typer.echo("Database Error!",err=True)
                typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                raise typer.Exit(code=1)
            user = list(answerMsg['Enteries'])
            if (len(user)==0):
                typer.echo("User with this Email {0} is not found in the stage table.".format(deletedUserEmail),err=True)
                return 1
            
            answerMsg = add_entry_one(database_name=k8sGroup,table_name="isolated_users",data=user[0])
            if('ErrorCode' in answerMsg):
                if(answerMsg['ErrorCode'] == '701'):        
                    typer.echo("Error: An user {0} exists on the Isolated Users table!".format(deletedUserEmail),err=True)
                    continue
                else:
                    typer.echo("The user {0} can't be moved to Isolated User Table.".format(deletedUserEmail),err=True)
                    typer.echo("Database Error!",err=True)
                    typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                    raise typer.Exit(code=1)
            
            answerMsg = CM_delete.delete_user_by_email(database_name=k8sGroup,table_name='stage',email=deletedUserEmail)
            if('ErrorCode' in answerMsg):
                typer.echo("The user {0} can't be removed from Stage Table.".format(deletedUserEmail),err=True)
                typer.echo("Database Error!",err=True)
                typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                raise typer.Exit(code=1)
            typer.echo("The User {0} is moved to Isolated table and you can't assign any role to it.".format(deletedUserEmail))
            answerMsg = CM_delete.delete_user_by_email(database_name=k8sGroup,table_name='user',email=deletedUserEmail)
            if('ErrorCode' in answerMsg):
                typer.echo("The user {0} can't be removed from User Table.".format(deletedUserEmail),err=True)
                typer.echo("Database Error!",err=True)
                typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                raise typer.Exit(code=1)
    else:
        typer.echo("No user was deleted from {0} group. No candidate to delete!".format(k8sGroup))

    # These data and users will be added to the stage table
    StageUserList = get_stage_table_enteries(stageCandidateList=userCandidateForStage)
    if(len(StageUserList)>0):
        typer.echo("The following users will be added to the Stage : ")
        i = 1
        for stageUser in StageUserList:
            stageUserEmail = stageUser['email']
            typer.echo("User {0} >>>  Email : {1} | DN : {2} ".format(i,stageUser['email'],stageUser['user_dn']))
            i = i + 1
            # When an isolated user back to k8s group it should be deleted from the isoalted user table
            answerMsg = CM_query.query_user_by_email(database_name=k8sGroup,table_name='isolated_users',email=stageUserEmail)
            if('ErrorCode' in answerMsg):
                typer.echo("Database Error!",err=True)
                typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                raise typer.Exit(code=1)
            user = list(answerMsg['Enteries'])
            if (len(user) > 0):
                answerMsg = CM_delete.delete_user_by_email(database_name=k8sGroup,table_name='isolated_users',email=stageUserEmail)
                if('ErrorCode' in answerMsg):
                    typer.echo("Database Error!",err=True)
                    typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
                    raise typer.Exit(code=1)
            else:
                continue
        # Add enteries to the STAGE
        add_entry_multiple(table_name="stage",database_name=k8sGroup,data=StageUserList)
    else:
        typer.echo("The Stage is up to date. No user will be added to.")

    #delete the pre_user table at the end
    preUserTable = get_collection(collection_name="pre_user",db_name=k8sGroup)
    preUserTable.drop()

