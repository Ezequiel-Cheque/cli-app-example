import click
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    

from modules import createController, createDTO, createService


def integration(filename: str):
    # click.echo(filename)
    doc={}
    with open(filename) as fichero:
        doc=load(fichero, Loader=Loader)
    
    click.echo(doc)
    
    # createController(name=name, path=path)
    # createService(name=name, path=path)
    # createDTO(name=name, path=path)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('integration_file', type=click.Path(exists=True))
def integrate(integration_file):
    # path = "."
    integration(filename=integration_file)

if __name__ == '__main__':
    cli()