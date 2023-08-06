from click.exceptions import ClickException
import typer
from christis.vars import *
from pathlib import Path

app = typer.Typer()


@app.command()
def cli():
    """
    View ChristisCLI Configuration
    """
    cliConfigPath = get_christis_cli_config_location()

    if (not Path(cliConfigPath).is_file()):
        typer.echo("ERROR: The cli.yaml file can't be found please use CLI to generate it!",err=True)
        raise typer.Exit(code=1)
    
    typer.echo("Open CLI Configuration File in {0}".format(cliConfigPath))
    typer.echo("\n")
    with open(cliConfigPath) as cli:
    # Here f is the file-like object
        read_data = cli.read()
        typer.echo(read_data)

@app.command()
def christis_API():
    """
    View ChristisAPI Configuration
    """
    christisAPIconfigPath = get_christis_api_config_location()

    if (not Path(christisAPIconfigPath).is_file()):
        typer.echo("ERROR: The cli.yaml file can't be found please use CLI to generate it!",err=True)
        raise typer.Exit(code=1)
    
    typer.echo("Open CLI Configuration File in {0}".format(christisAPIconfigPath))
    typer.echo("\n")
    with open(christisAPIconfigPath) as api:
    # Here f is the file-like object
        read_data = api.read()
        typer.echo(read_data)

@app.command()
def database():
    """
    View MongoDB Configuration
    """
    christisMongoconfigPath = get_mongo_configuration_location()

    if (not Path(christisMongoconfigPath).is_file()):
        typer.echo("ERROR: The cli.yaml file can't be found please use CLI to generate it!",err=True)
        raise typer.Exit(code=1)
    
    typer.echo("Open CLI Configuration File in {0}".format(christisMongoconfigPath))
    typer.echo("\n")
    with open(christisMongoconfigPath) as mongo:
    # Here f is the file-like object
        read_data = mongo.read()
        typer.echo(read_data)