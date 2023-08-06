from click.termui import confirm
import typer
import yaml
from pathlib import Path
from christis.vars import *
import os


app = typer.Typer()

@app.command()
def cli(
    api_address: str = typer.Option(...,"--api-address",envvar="CHRISTIS_API_ADDRESS",help="Christis API Server Address"),
    api_port: str = typer.Option(...,"--api-port",envvar="CHRISTIS_API_PORT",help="Christis API Server Port"),
    k8s_group: str = typer.Option(...,"--k8s-group",envvar="CHRISTIS_K8s_LDAP_GROUP",help="The group that its user should access to K8s cluster"),
    ):

    """
    Generate a ChristisCLI configuration file in the ~/.christisCLI location
    """

    if not Path(get_mongo_configuration_location()).is_file():
        typer.echo(f"The Database config file is not found. Please generate it via CLI and try again.",err=True)
        raise typer.Abort()
    config = {}
    config['ChristisCLI'] = {}
    CLI_Config_Location = get_christis_config_location()
    configFileLocation = "{0}{1}".format(CLI_Config_Location,"cli.yaml")
    if Path(configFileLocation).is_file():
        overwrite = typer.confirm("The CLI configuration exists, Do you want to generate it again?")
        if not overwrite:
            typer.echo("Not Generating New Configuration File")
            raise typer.Abort()
    typer.echo("Generate New Config File")
    config['ChristisCLI']["CHRISTIS_API_ADDRESS"] = api_address
    config['ChristisCLI']["CHRISTIS_API_PORT"] = api_port
    config['ChristisCLI']["CHRISTIS_K8s_LDAP_GROUP"] = k8s_group
    config['ChristisCLI']["CHRISTIS_MONGO_CONFIG_FILE"] = get_mongo_configuration_location()

    if not os.path.exists(CLI_Config_Location):
        os.makedirs(CLI_Config_Location)
    try:
        
        with open(configFileLocation,'w') as file:
            configFile = yaml.dump(config,file)
    except Exception as e:
        typer.echo(e,err=True)
        raise typer.Abort()     


@app.command()
def database(
    mongo_address: str = typer.Option(...,"--mongodb-address",envvar="MONGODB_ADDRESS",help="The address of MongoDB"),
    mongo_user: str = typer.Option(...,"--mongodb-user",envvar="MONGODB_USER",help="The username that access to database"),
    mongo_password: str = typer.Option(...,"--mongodb-password",help="The password of user who access the database"),
):
    """
    Generate MongoDB configuration file that need to access database in the ~/.christisCLI location
    """
    config = {}
    config["MongoDB"] = {}

    CLI_Config_Location = get_christis_config_location()
    configFileLocation = "{0}{1}".format(CLI_Config_Location,"mongo.yaml")
    if Path(configFileLocation).is_file():
        overwrite = typer.confirm("The MongoDB configuration exists, Do you want to generate it again?")
        if not overwrite:
            typer.echo("Not Generating New Configuration File")
            raise typer.Abort()
    typer.echo("Generate New Config File")
    config["MongoDB"]["mongo_address"] = mongo_address
    config["MongoDB"]["mongo_user"] = mongo_user
    config["MongoDB"]["mongo_password"] = mongo_password

    if not os.path.exists(CLI_Config_Location):
        os.makedirs(CLI_Config_Location)
    try:
        with open(configFileLocation,'w') as file:
            configFile = yaml.dump(config,file)
    except Exception as e:
        typer.echo(e,err=True)
        raise typer.Abort()

@app.command()
def christis_API(
    ldap_server: str = typer.Option(...,"--ldap-server-address",help="The LDAP server address. Should be in this format LDAP://<Address>"),
    ldap_user_connector: str = typer.Option(...,"--ldap-user",help="The User DN that can access to server to query like  CN=Administrator,CN=Users,DC=cloudarmin,DC=local"),
    ldap_password_connector: str = typer.Option(...,"--ldap-password",help="The password of user who access to server"),
    ldap_base_dn: str = typer.Option(...,"--ldap-base-dn",help="The base DN of you LDAP domain like dc=cloudarmin,dc=local"),
    ldap_k8s_group: str = typer.Option(...,"--ldap-k8s-group",help="The cn of group that its users should access the K8s cluster")):

    """
    Generate ChristisCLI configuration file that will be used by ChristisAPI Docker container in the ~/.christisCLI location
    """
    config = {}
    config["ldap"] = {}

    CLI_Config_Location = get_christis_config_location()
    configFileLocation = "{0}{1}".format(CLI_Config_Location,"ldap.yaml")
    if Path(configFileLocation).is_file():
        overwrite = typer.confirm("The LDAP configuration exists, Do you want to generate it again?")
        if not overwrite:
            typer.echo("Not Generating New Configuration File")
            raise typer.Abort()
    typer.echo("Generate New Config File")

    config["ldap"]["ldap_server"] = ldap_server
    config["ldap"]["ldap_user_connector"] = ldap_user_connector
    config["ldap"]["ldap_password_connector"] = ldap_password_connector
    config["ldap"]["ldap_base_dn"] = ldap_base_dn
    config["ldap"]["ldap_k8s_group"] = ldap_k8s_group

    if not os.path.exists(CLI_Config_Location):
        os.makedirs(CLI_Config_Location)
    try:
        with open(configFileLocation,'w') as file:
            configFile = yaml.dump(config,file)
    except Exception as e:
        typer.echo(e,err=True)
        raise typer.Abort()