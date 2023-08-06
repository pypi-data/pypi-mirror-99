import typer
import christis.cmd_user.role as role
import christis.cmd_user.view as view

app = typer.Typer()
app.add_typer(role.app,name="role",help="Commands related to assign,unassign,and view user role")
app.add_typer(view.app,name="view",help="Commands relate to view user and its information")