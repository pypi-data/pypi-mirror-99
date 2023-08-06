import typer
from ChristisMongo.table.get import *  
import os , json
from tabulate import tabulate
from typing import Optional

app = typer.Typer()

@app.command()
def stage(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
         jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")):
    """
    View Stage table
    """

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    answerMsg = get_all_entries(database_name=k8sGroup,table_name="stage")

    if('ErrorCode' in answerMsg):

        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)
    
    stageUser = list(answerMsg['Enteries'])

    if (jsson):
        typer.echo(json.dumps(stageUser))
        typer.Exit(code=0)
        return

    if ( not all and verbose == 0):
        simpleView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            simpleView.append(tempList)
        typer.echo(tabulate(simpleView,tablefmt="pretty",headers=["Emails"]))
    
    if (not all and verbose == 1):

        normalView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            normalView.append(tempList)
        typer.echo(tabulate(normalView,tablefmt="pretty",headers=["Emails","User CN"]))

    if ( not all and verbose == 2):

        extendedView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            tempList.append(user['user_dn'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["Emails","User CN","User DN"]))
    
    if ( all or verbose > 2):
        extendedView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['_id'])
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            tempList.append(user['user_dn'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["ID","Emails","User CN","User DN"]))

@app.command()
def user(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
         jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")):
    """
    View User table
    """

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    answerMsg = get_all_entries(database_name=k8sGroup,table_name="user")

    if('ErrorCode' in answerMsg):

        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)
    
    users = list(answerMsg['Enteries'])

    if (jsson):
        typer.echo(json.dumps(users))
        typer.Exit(code=0)
        return

    if ( not all and verbose == 0):
        simpleView = []
        for user in users:
            tempList = []
            tempList.append(user['email'])
            simpleView.append(tempList)
        typer.echo(tabulate(simpleView,tablefmt="pretty",headers=["Emails"]))
    
    if (not all and verbose == 1):

        normalView = []
        for user in users:
            tempList = []
            tempList.append(user['email'])
            tempList.append(user['user_dn'])
            normalView.append(tempList)
        typer.echo(tabulate(normalView,tablefmt="pretty",headers=["Emails","User DN"]))

    if ( all or verbose == 2):

        extendedView = []
        for user in users:
            tempList = []
            tempList.append(user['_id'])
            tempList.append(user['email'])
            tempList.append(user['user_dn'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["ID","Emails","User DN"]))

@app.command()
def main(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
        jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")
):
    """
    View Main table
    """
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    answerMsg = get_all_entries(database_name=k8sGroup,table_name="main")

    if('ErrorCode' in answerMsg):

        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)

    roleAssignments = list(answerMsg['Enteries'])
    if (jsson):
        typer.echo(json.dumps(roleAssignments))
        typer.Exit(code=0)
        return
    
    if ( not all and verbose == 0):
        simpleView = []
        for role in roleAssignments:
            tempList = []
            tempList.append(role['user_email'])
            tempList.append(role['user_cn'])
            tempList.append(role['role_name'])
            tempList.append(role['role_version'])            
            tempList.append(role['release_name'])
            simpleView.append(tempList)
        typer.echo(tabulate(simpleView,tablefmt="pretty",headers=["User Email","User CN","Role Name","Role Version","Release Name"]))
    
    if (not all and verbose == 1):

        normalView = []
        for role in roleAssignments:
            tempList = []
            tempList.append(role['user_email'])
            tempList.append(role['user_cn'])
            tempList.append(role['user_dn'])
            tempList.append(role['role_name'])
            tempList.append(role['role_version'])            
            tempList.append(role['release_name'])
            normalView.append(tempList)
        typer.echo(tabulate(normalView,tablefmt="pretty",headers=["User Email","User CN","User DN","Role Name","Role Version","Release Name"]))

    if ( all or verbose == 2):

        extendedView = []
        for role in roleAssignments:
            tempList = []
            tempList.append(role['_id'])
            tempList.append(role['user_id'])
            tempList.append(role['user_email'])
            tempList.append(role['user_cn'])
            tempList.append(role['user_dn'])
            tempList.append(role['role_name'])
            tempList.append(role['role_version'])            
            tempList.append(role['release_name'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["Assignment ID","User ID","User Email","User CN","User DN","Role Name","Role Version","Release Name"]))

@app.command()
def isolated(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
         jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")):
    """
    View Isolated Users table
    """
    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']

    answerMsg = get_all_entries(database_name=k8sGroup,table_name="isolated_users")

    if('ErrorCode' in answerMsg):

        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)
    
    stageUser = list(answerMsg['Enteries'])

    if (jsson):
        typer.echo(json.dumps(stageUser))
        typer.Exit(code=0)
        return

    if ( not all and verbose == 0):
        simpleView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            simpleView.append(tempList)
        typer.echo(tabulate(simpleView,tablefmt="pretty",headers=["Emails"]))
    
    if (not all and verbose == 1):

        normalView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            normalView.append(tempList)
        typer.echo(tabulate(normalView,tablefmt="pretty",headers=["Emails","User CN"]))

    if ( not all and verbose == 2):

        extendedView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            tempList.append(user['user_dn'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["Emails","User CN","User DN"]))
    
    if ( all or verbose > 2):
        extendedView = []
        for user in stageUser:
            tempList = []
            tempList.append(user['_id'])
            tempList.append(user['email'])
            tempList.append(user['user_cn'])
            tempList.append(user['user_dn'])
            extendedView.append(tempList)
        typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["ID","Emails","User CN","User DN"]))

