import typer

app = typer.Typer()

@app.callback()
def callback():
    """
    TG Tools
    """

@app.command()
def categories(url: str):
    """
    Список категорий
    """
    typer.echo(f"Hello {name} {lastname}")


if __name__ == "__main__":
    app()










