import typer
import christis.cmd_database.view as db_view
from typing import Optional


app = typer.Typer()

@app.command()
def stage(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
         jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")):
    """
    View users in the stage table
    """

    db_view.stage(verbose=verbose,all=all,jsson=jsson)

@app.command()
def main(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
        jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")
):
    """
    View users in the main table
    """
    db_view.main(verbose=verbose,all=all,jsson=jsson)

@app.command()
def isolated(verbose: int = typer.Option(0,"--verbose","-v",count=True),
         all: bool = typer.Option(False, "--all"),
         jsson: Optional[bool] = typer.Option(False, "--json",help="Output format in Json")):
    """
    View users in the isolated users table
    """

    db_view.isolated(verbose=verbose,all=all,jsson=jsson)