import dotenv

dotenv.load_dotenv()
import click
import rich
import models
import db

db.create_db_and_tables()


@click.group()
def app():
    pass


@app.command()
@click.option("--op1", default=500, help="Limit the number of markets returned.")
def command(op1):
    rich.print([op1]*20)

if __name__ == "__main__":
    app()
