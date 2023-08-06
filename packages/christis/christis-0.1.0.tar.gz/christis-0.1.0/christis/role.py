import typer
from pathlib import Path
from typing import Optional
import subprocess
import os 
from shutil import which
from christis.engine.core.general import get_sha2
import yaml
import ChristisMongo.table.add as CM_add
from tabulate import tabulate
from ChristisMongo.table.get import *
import ChristisMongo.table.query as CM_query


app = typer.Typer()

@app.callback()
def main(ctx: typer.Context):

    if(ctx.invoked_subcommand != 'create'):
         return
    
    if (which('helm') == None):
        typer.echo("ERROR: Helm is not found! Please install it.",err=True)
        raise typer.Exit(code=1)

@app.command()
def create(
    name: str = typer.Option(...,"--name",help="The role name"),
    location: Path = typer.Option(...,"--location",help="The location of Helm Chart that specifies your role. Can be in .tgz or folder"),
    description: str = typer.Option(...,"--description",help="A description for your role"),
    version: str = typer.Option(...,"--version",help="The role version"),
    varFile : Optional[Path] = typer.Option(None,"--var-file",help="The variable file that the role needs besides of the variables that are provided by CLI")
):
    """
    Create a Role from Helm Chart and save it in the Database
    """
    if location.is_file():
        filename, file_extension = os.path.splitext(location)

        if (not file_extension == '.tgz'):
            typer.echo("ERROR: The role file is not in proper package format",err=True)
            raise typer.Exit(code=1)
    #TODO : Check varfile exist!?
    if varFile is None:
        varFile = "None"
    else:
        if varFile.is_dir():
            typer.echo("ERROR: The var file is directory should be file!",err=True)
            raise typer.Exit(code=1)
        
        varFileName, varExt = os.path.splitext(varFile)

        if(not(varExt == 'yml' or varExt == 'yaml')):
            typer.echo("ERROR: The var file should be yaml or yml",err=True)
            raise typer.Exit(code=1)
        
        with open(varFile, 'r') as stream:
            try:
                pass
            except yaml.YAMLError as exc:
                typer.echo("ERROR: The var file couldn't be read",err=True)
                raise typer.Exit(code=1)
    
    Lint_out = subprocess.Popen(['helm', 'lint', location], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = Lint_out.communicate()

    if (Lint_out.returncode == 1):
        typer.echo("ERROR: The role's linting is faild.")
        typer.echo("\n")
        typer.echo(stdout.decode('utf-8'))
        raise typer.Exit(code=1)
    else:
        typer.echo("Role's linting is sucessful.")
    
    roleID = get_sha2("{0}-{1}".format(name,version))
    
    role = {
        "_id": roleID,
        "role_name": name,
        "location": str(location),
        "version" : str(version),
        "var_file" : str(varFile),
        "description" : description
    }

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']
    result = CM_add.add_entry_one(database_name=k8sGroup,table_name='role',data=role)

    if ('ErrorCode' in result):
        if(result['ErrorCode'] == '701'):
            typer.echo("ERROR: The role with these name and version exists. Role can't be added",err=True)
            raise typer.Exit(code=1)
        else:
            typer.echo("ERROR: Error Message : {0}.".format(result['ErrorMsg']),err=True)
            raise typer.Exit(code=1)

@app.command()
def view(
    name: Optional[str] = typer.Option(None,"--name",help="The role name"),
    verbose: int = typer.Option(0,"--verbose","-v",count=True),
):

    """
    View the Roles that are already available
    """

    k8sGroup = os.environ['CHRISTIS_K8s_LDAP_GROUP']
    answerMsg = get_all_entries(database_name=k8sGroup,table_name='role')

    if('ErrorCode' in answerMsg):

        typer.echo("Database Error!",err=True)
        typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
        raise typer.Exit(code=1)
    
    roles = list(answerMsg['Enteries'])

    if(name is None):
        if(verbose == 0):
            normalView = []
            for role in roles:
                tempList = []
                tempList.append(role['role_name'])
                tempList.append(role['location'])
                tempList.append(role['version'])
                normalView.append(tempList)
            typer.echo(tabulate(normalView,tablefmt="pretty",headers=["Role Name","Location","Version"]))
        if(verbose > 0):
            extendedView = []
            for role in roles:
                tempList = []
                tempList.append(role['_id'])
                tempList.append(role['role_name'])
                tempList.append(role['location'])
                tempList.append(role['version'])
                tempList.append(role['var_file'])
                extendedView.append(tempList)
            typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["ID","Role Name","Location","Version","VarFile Path"]))

    else:
        answerMsg = CM_query.query_role_by_roleName(database_name=k8sGroup,table_name='role',role=name)
        if('ErrorCode' in answerMsg):
            typer.echo("Database Error!",err=True)
            typer.echo("Error Message : {0}".format(answerMsg['ErrorMsg']),err=True)
            raise typer.Exit(code=1)
        roles = list(answerMsg['Enteries'])
        if(len(roles)==0):
            typer.echo("Role with the name of '{0}' is not found".format(name),err=True)
            raise typer.Exit(code=1)
        else:
            if(verbose == 0):
                normalView = []
                for role in roles:
                    tempList = []
                    tempList.append(role['role_name'])
                    tempList.append(role['location'])
                    tempList.append(role['version'])
                    normalView.append(tempList)
                typer.echo(tabulate(normalView,tablefmt="pretty",headers=["Role Name","Location","Version"]))
            if(verbose > 0):
                extendedView = []
                for role in roles:
                    tempList = []
                    tempList.append(role['_id'])
                    tempList.append(role['role_name'])
                    tempList.append(role['location'])
                    tempList.append(role['version'])
                    tempList.append(role['var_file'])
                    extendedView.append(tempList)
                typer.echo(tabulate(extendedView,tablefmt="pretty",headers=["ID","Role Name","Location","Version","VarFile Path"]))







