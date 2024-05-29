import click

@click.group()
def cli():
    pass

def createService():
    click.echo("Service created")

def createController():
    click.echo("Controller created")

@cli.command()
@click.option('-co', '--controller', "controller", default=None, help="Create a controller")
@click.option('-s', '--service', "service", default=None, help="Create a service")
def generate(controller, service):
    click.echo(controller)
    click.echo(service)


if __name__ == '__main__':
    cli()