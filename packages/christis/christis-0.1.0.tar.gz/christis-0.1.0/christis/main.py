import typer
from christis.vars import *
import christis.config as config
import christis.database as database
import christis.user as user
from christis.utils.general import set_env
from pathlib import Path
from christis.utils.config_parser import get_configuration
import os 
import ChristisRequestor.user as CR_user
import christis.role as role

app = typer.Typer()
app.add_typer(config.app,name="config",help="Commands related to configuration generator")
app.add_typer(database.app,name="database",help="Commands relate to databsae sync and view tables")
app.add_typer(user.app,name="user",help="Commands related to user and its roles")
app.add_typer(role.app,name="role",help="Commands related to role")

@app.callback()
def main(ctx: typer.Context):
    """
    Christis CLI \n
    A Command-Line tool to manage users on Kubernetes cluster
    """
    if (ctx.invoked_subcommand == "config"):
        return
    
    mongoConfigPath = get_mongo_configuration_location()
    cliConfigPath = get_christis_cli_config_location()
    if (not Path(mongoConfigPath).is_file()):
        typer.echo("ERROR: The mongo.yaml file can't be found please use CLI to generate it!",err=True)
        raise typer.Exit(code=1)

    if (not Path(cliConfigPath).is_file()):
        typer.echo("ERROR: The cli.yaml file can't be found please use CLI to generate it!",err=True)
        raise typer.Exit(code=1)
    
    cliConfiguration = get_configuration(cliConfigPath)
    if('ErrorCode' in cliConfiguration):
        typer.echo("ERROR: ldap.yaml",err=True)
        typer.echo(cliConfiguration['ErrorMsg'],err=True)
        typer.Abort()
        raise typer.Exit(code=1)
    
    set_env(cliConfiguration['ChristisCLI'])

app()