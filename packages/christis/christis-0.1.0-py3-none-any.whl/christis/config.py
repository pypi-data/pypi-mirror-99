import typer
import christis.cmd_config.generate as generate
import christis.cmd_config.view as view

app = typer.Typer()

app.add_typer(generate.app,name="generate",help="Christis components configuration generators")
app.add_typer(view.app,name="view",help="View Christis components configurations")