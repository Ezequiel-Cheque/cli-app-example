import click

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo("Initialized the DataBase")
    
@cli.command()
def dropdb():
    click.echo("Dropped the database")

@cli.command()
@click.option('--count', default=5, help='Number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}")

if __name__ == '__main__':
    cli()