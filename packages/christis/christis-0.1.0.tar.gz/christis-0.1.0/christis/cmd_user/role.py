from pymongo import results
import typer
from typing import List, Optional
import os
from ChristisMongo.table.get import *
from enum import Enum
from ChristisMongo.table.query import *
import subprocess
from pathlib import Path
import yaml , json
from christis.engine.core.general import get_domain_part_from_dn, get_sha2
from ChristisMongo.table.add import *
from ChristisMongo.table.delete import *
from tabulate import tabulate


app = typer.Typer()
exportcmd = typer.Typer()
importcmd = typer.Typer()
app.add_typer(importcmd,name="import",help="import template for bulk role assignment")
app.add_typer(exportcmd,name="export",help="export a template from stage user for bulk role assignment")

class attributeType (str, Enum):
    dn = "dn"
    cn = "cn"
    email = "email"
    #id = "id"

@app.command()
def view(
    user_attr: str = typer.Option(...,'--attribute-value',help='The user attribute value that is used to find user'),
    attr_type : attributeType = typer.Option(...,'--attribute-type',help="The attribute type of user-attribute",case_sensitive=False),
    role: Optional[str] = typer.Option(None,"--role",help="the role name"),
    verbose: int = typer.Option(0,"--verbose","-v",count=True),
    jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")
):

    """
    View the users role assignment 
    """

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    if(role is None):

        query = {"user_{0}".format(attr_type): user_attr}
    else:
        query = {"user_{0}".format(attr_type): user_attr,"role_name":role}

    answerMsg = query_abstract(database_name=k8sGroup,table_name='main',query=query)

    if('ErrorCode' in answerMsg):
        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)
    enteries = list(answerMsg['Enteries'])
    if(len(enteries)==0):
        typer.echo("The user with the attribute value of {0} and attribute type of {1} is not found. No role assignemet!".format(user_attr,attr_type))
        raise typer.Exit(code=1)
    
    if (jsson):
        typer.echo(json.dumps(enteries))
        typer.Exit(code=0)
        return

    if(verbose==0):
        normalView = []
        for entry in enteries:
            tempList = []
            tempList.append(entry['user_email'])
            tempList.append(entry['user_cn'])
            tempList.append(entry['user_dn'])
            tempList.append(entry['role_name'])
            tempList.append(entry['role_version'])
            tempList.append(entry['release_name'])
            normalView.append(tempList)
            typer.echo(tabulate(normalView,tablefmt="pretty",headers=["User Email","User CN","User DN","Role Name","Role Version","Release Name"]))
    if(verbose>=1):
        extendedView = []
        for entry in enteries:
            tempList = []
            tempList.append(entry['_id'])
            tempList.append(entry['user_id'])
            tempList.append(entry['user_email'])
            tempList.append(entry['user_cn'])
            tempList.append(entry['user_dn'])
            tempList.append(entry['role_name'])
            tempList.append(entry['role_version'])
            tempList.append(entry['release_name'])
            extendedView.append(tempList)
            typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["Assignment ID","User ID","User Email","User CN","User DN","Role Name","Role Version","Release Name"]))


@app.command()
def assign (
    user_attr: str = typer.Option(...,'--attribute-value',help='The user attribute value that is used to find and assign role to user'),
    attr_type : attributeType = typer.Option(...,'--attribute-type',help="The attribute type of user-attribute",case_sensitive=False),
    roleList: List[str] = typer.Option(...,'--role',help='The role name and version that should be assigned to user. should be in this format <RoleName>*<RoleVersion>'),
    varFile: Optional[Path] = typer.Option(None,"--override-var-file",help="The variable file that override the default variable file of Role")
):
    """
    Assign Role to the User
    """
    
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']
    user = []
    if(attr_type == 'dn'):
        answerMsg = query_user_by_dn(database_name=k8sGroup,table_name='stage',dn=user_attr)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        user = list(answerMsg['Enteries'])
        if (len(user)==0):
            typer.echo("User with this of DN {0} is not found in the stage table.".format(user_attr),err=True)
            return 1
    
    if(attr_type == 'cn'):
        answerMsg = query_user_by_cn(database_name=k8sGroup,table_name='stage',cn=user_attr)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        user = list(answerMsg['Enteries'])
        if (len(user)==0):
            typer.echo("User with the CN of {0} is not found in the stage table.".format(user_attr),err=True)
            return 1
    
    if(attr_type == 'email'):
        answerMsg = query_user_by_email(database_name=k8sGroup,table_name='stage',email=user_attr)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        user = list(answerMsg['Enteries'])
        if (len(user)==0):
            typer.echo("User with the Email of {0} is not found in the stage table.".format(user_attr),err=True)
            return 1
    
    if(attr_type == 'id'):
        answerMsg = query_user_by_id(database_name=k8sGroup,table_name='stage',id=user_attr)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        user = list(answerMsg['Enteries'])
        if (len(user)==0):
            typer.echo("User with the Id of {0} is not found in the stage table.".format(user_attr),err=True)
            return 1
    
    approvedRole = {}

    # Check VarFile
    if varFile is None:
        varFile = "None"
    else:
        if varFile.is_dir():
            typer.echo("ERROR: The var file is directory should be file!",err=True)
            raise typer.Exit(code=1)
        
        varFileName, varExt = os.path.splitext(varFile)

        if(not(varExt == '.yml' or varExt == '.yaml')):
            typer.echo("ERROR: The var file should be yaml or yml",err=True)
            raise typer.Exit(code=1)
        
        with open(varFile, 'r') as stream:
            try:
                pass
            except yaml.YAMLError as exc:
                typer.echo("ERROR: The var file couldn't be read",err=True)
                raise typer.Exit(code=1)
    

    for role in roleList:

        if "*" not in role:
            typer.echo("Error: Bad role format. It should be in this format <RoleName>*<RoleVersion>")
            raise typer.Exit(code=1)

        roleName = role.split('*')[0]
        roleVersion = role.split("*")[1]

        query = {"role_name" : roleName, "version": roleVersion}

        answerMsg = query_abstract(database_name=k8sGroup,table_name='role',query=query)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        roleQ = list(answerMsg['Enteries'])
        if(len(roleQ)==0):
            typer.echo("The role with the name of {0} and version of {1} is not found! Failed to assign the role.".format(roleName,roleVersion))
            return 1
        if(varFile is None):
            approvedRole[roleName] = {'version':roleVersion,'path':roleQ[0]['location'],'varFile':roleQ[0]['var_file'],'id':roleQ[0]['_id']}
        else:
            approvedRole[roleName] = {'version':roleVersion,'path':roleQ[0]['location'],'varFile':varFile,'id':roleQ[0]['_id']}
        
    #UserDetails
    userCN = user[0]['user_cn']
    userDN = user[0]['user_dn']
    userEmail = user[0]['email']
    userId = user[0]['_id']

    typer.echo("Assigning Role to the user: {1}={0} ...".format(user_attr,attr_type))
    with typer.progressbar(approvedRole.items(),label="Processing") as progress:
        for r in progress:
            roleName = r[0]
            roleVersion = r[1]['version']
            roleId = r[1]['id'] 
            # releaseName = <group>-cn-dc-rolename-roleversion
            userDomainPart = get_domain_part_from_dn(userDN)
            releaseName = "{0}-{1}-{2}-{3}-{4}".format(k8sGroup,userCN.replace(" ", ""),userDomainPart,roleName.replace(" ", ""),roleVersion.replace(" ", "")) # remove the space from the rolename and version and user CN
            CNvariable = 'user_cn={0}'.format(userCN)
            typer.echo("ReleaseName : {0}".format(releaseName))
            # Have to !
            DNvariable = 'user_dn={0}'.format(userDN.replace('=',':').replace(',','-'))
            EmailVariable = 'user_email={0}'.format(userEmail)
            IDvariable = 'user_id={0}'.format(userId)
            GroupVariable = 'user_k8_group={0}'.format(k8sGroup)

            # check the helm release is exist or not
            checkCommand = ['helm','list','-o','json','--filter',releaseName]

            checkOut = subprocess.Popen(checkCommand,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            chkStdOut , chkStdErr = checkOut.communicate()

            if(checkOut.returncode == 1):
                typer.echo("ERROR: The Release existance checking faild.")
                typer.echo("\n")
                typer.echo(chkStdOut.decode('utf-8'))
                raise typer.Exit(code=1)
            
            jsonChk = json.loads(chkStdOut.decode('utf-8'))
            if( len(jsonChk) > 0):
                typer.echo("ERROR: A release with the name of ' {0} ' exists that is using the role of ' {1} ' with version of ' {2} '.".format(releaseName,roleName,roleVersion))
                typer.Abort()
                continue

            if(r[1]['varFile']=='None'):
                command = ['helm','install',releaseName,"--set",CNvariable,"--set",DNvariable,"--set",EmailVariable,"--set",IDvariable,"--set",GroupVariable,r[1]['path']]
            else:
                command = ['helm','install',releaseName,"--set",CNvariable,"--set",DNvariable,"--set",EmailVariable,"--set",IDvariable,"--set",GroupVariable,"-f",r[1]['varFile'],r[1]['path']]
            out = subprocess.Popen(command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

            stdout,stderr = out.communicate()
            if (out.returncode == 1):
                typer.echo("ERROR: The role assignment is faild.")
                typer.echo("\n")
                typer.echo(stdout.decode('utf-8'))
                raise typer.Exit(code=1)
            else:
                typer.echo("The role {0} with the version of {1} is assigned.".format(roleName,roleVersion))
            
            releaseID = get_sha2(releaseName)

            mainEntry = {"_id":releaseID,"user_id":userId,"user_email":userEmail,"user_cn":userCN,"user_dn":userDN,"role_name":roleName,"role_version":roleVersion,"role_id":roleId,'release_name':releaseName}
            answerMsg = add_entry_one(database_name=k8sGroup,data=mainEntry,table_name='main')
            
            if('ErrorCode' in answerMsg):
                uninstallCommand = ['helm','uninstall',releaseName]
                outUninstall = subprocess.Popen(uninstallCommand, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
                typer.echo("Error! Release will be uinstalled!",err=True)
                if(answerMsg['ErrorCode'] == '701'):        
                    typer.echo("Error: A release with this Id exists on the Main table!",err=True)
                    continue
                else:
                    typer.echo("Error : {0}".format(answerMsg['ErrorMsg']),err=True)
                    raise typer.Exit(code=1)

@exportcmd.command()
def template(
    location: Path = typer.Option(...,"--location",help="The template's absolute path to export")
):
    """
    Export template
    """
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    answerMsg = get_all_entries(database_name=k8sGroup,table_name='stage')

    if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
    user = list(answerMsg['Enteries'])
    if (len(user)==0):
        typer.echo("There is no users in the stage table.",err=True)
        raise typer.Exit(code=1)
    
    template = []

    for u in user:
        userDict = { u['email']: {'role':{'role1':'version','role2':'version'},'variableFile':'location'}}
        template.append(userDict)

    with open(location, 'w') as file:
        documents = yaml.dump(template, file)

    typer.echo("Export Done!")
    typer.Exit(code=0)
                   
@importcmd.command()
def template(
    location: Path = typer.Option(...,"--location",help="The template's absolute path to export")
):  
    """
    Import Template
    """
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    if location.is_dir():
        typer.echo("ERROR: The var file is directory should be file!",err=True)
        raise typer.Exit(code=1)
        
    fileName, fileExt = os.path.splitext(location)
    if(not(fileExt == '.yml' or fileExt == '.yaml')):
        typer.echo("ERROR: The template file should be yaml or yml",err=True)
        raise typer.Exit(code=1)

    with open(location, 'r') as stream:
        try:
            users = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            typer.echo("ERROR: The tempate file couldn't be read: {0}".format(exc),err=True)
            raise typer.Exit(code=1)
    
    with typer.progressbar(users) as progress:
        for user in progress:
            for email in user:
                
                roles = user[email]['role']
                for role,version in  roles.items():
                    typer.echo("\n")
                    typer.echo("*********************************************************")
                    typer.echo("\n")
                    if(user[email]['variableFile'] == 'None'):
                        result = assign(attr_type="email",roleList=["{0}*{1}".format(role,version)],user_attr=email,varFile=None)
                    else:
                        result = assign(attr_type="email",roleList=["{0}*{1}".format(role,version)],user_attr=email,varFile=user[email]['variableFile'])
                    if(result == 1):
                        typer.echo("The role assignmnet for the role of {0} with the version of {1} to the user {2} is failed.".format(role,version,email))

@app.command()
def unassign(
    user_attr: str = typer.Option(...,'--attribute-value',help='The user attribute value that is used to find and unassign role from user'),
    attr_type : attributeType = typer.Option(...,'--attribute-type',help="The attribute type of user-attribute",case_sensitive=False),
    role: str = typer.Option(...,'--role',help='The role name and version that should be unassigned from user. should be in this format <RoleName>*<RoleVersion> . ALL can be used to unassign all roles.')):
    """
    Unassign a Role from user 
    """
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    if (role != "ALL" and "*" not in role):
            typer.echo("Error: Bad role format. It should be in this format <RoleName>*<RoleVersion>")
            raise typer.Exit(code=1)

    roleName = ""
    roleVersion = ""
    if(role == "ALL"):
        query = {"user_{0}".format(attr_type): user_attr}
    else:
        roleName = role.split('*')[0]
        roleVersion = role.split("*")[1]
        query = {"user_{0}".format(attr_type): user_attr,"role_name":roleName,"role_version":roleVersion}

    answerMsg = query_abstract(database_name=k8sGroup,table_name='main',query=query)

    if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
    assignmentEnteries = list(answerMsg['Enteries'])
    if(len(assignmentEnteries)==0):
        if(role != "ALL"):
            typer.echo("The role assignment for user {0}: {1} and role: {2} and version: {3} is not found!".format(attr_type,user_attr,roleName,roleVersion),err=True)
            return 1
        else:
            typer.echo("No role assignment for the user {0}: {1} is found!".format(attr_type,user_attr),err=True)
            return 1
    
    for assignment in assignmentEnteries:

        releaseName = assignment['release_name']
        assignmentID = assignment['_id']
        
        roleName = assignment['role_name']
        roleVersion = assignment['role_version']
        typer.echo("The release name : {0}".format(releaseName))
        deleteQuery = {"_id":assignmentID}
        answerMsg= delete_abstract_one(database_name=k8sGroup,query=deleteQuery,table_name='main')
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        
        uninstallCommand = ['helm','uninstall',releaseName]
        outUninstall = subprocess.Popen(uninstallCommand, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)

        stdout,stderr = outUninstall.communicate()
        if (outUninstall.returncode == 1):
            typer.echo("ERROR: The role unassigning is faild.")
            typer.echo("\n")
            typer.echo(stdout.decode('utf-8'))
            # return back the enteries to main table after failing uninstalling!
            add_entry_one(data=assignment,database_name=k8sGroup,table_name='main')
            raise typer.Exit(code=1)
        else:
            typer.echo("The role {0} with the version of {1} is unassigned.".format(roleName,roleVersion))

        

@app.command()
def purge(
    user_attr: str = typer.Option(...,'--attribute-value',help='The user attribute value that is used to find and purge role of isolated user'),
    attr_type : attributeType = typer.Option(...,'--attribute-type',help="The attribute type of user-attribute",case_sensitive=False)):
    """
    Unassign all roles of isoalted user 
    """
    if(attr_type == attributeType.email):
        query = {"email":user_attr}
    else:    
        query = {"user_{0}".format(attr_type): user_attr}

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']


    answerMsg = query_abstract(database_name=k8sGroup,table_name='isolated_users',query=query)

    if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
    assignmentEnteries = list(answerMsg['Enteries'])
    if(len(assignmentEnteries)==0):
        
        typer.echo("There is no user with this information {0} : {1} in the Isolated table!".format(attr_type,user_attr),err=True)
        return 1
    
    unassign(user_attr=user_attr,attr_type=attr_type,role='ALL')
    

