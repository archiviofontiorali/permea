from typer import Typer, echo

cli = Typer()


@cli.command()
def hello():
    echo(f"Hello, World!")


if __name__ == "__main__":
    cli()
