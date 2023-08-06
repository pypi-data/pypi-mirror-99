import typer
from ucode.ucode.ucode_srv import UCode

app = typer.Typer()


@app.command(name="upload")
def upload_problem_to_ucode(user_name: str):
    typer.echo(f"Creating user: {user_name}")


@app.command(name="login")
def login(email: str = typer.Argument(..., help='ucode.vn email'),
          password: str = typer.Argument(..., help='ucode.vn password'),
          env: str = typer.Option("prod", "--env", "-e",
                                   help='prod|dev for ucode environment'),
          ):
    ucode = UCode(env)
    ucode.login(email, password)


if __name__ == "__main__":
    app()