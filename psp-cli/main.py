import click
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    

from modules import createController, createDTO, createService


def integration(filename: str):
    try:
        doc={}
        with open(filename) as fichero:
            doc=load(fichero, Loader=Loader)
        
        click.echo(doc)
    except Exception as err:
        click.echo(f"Error, invalid yaml: {str(err)}");

    ## Crear Dto del psp
    ## agregar dto al init
    ## Crear service
    ## crear controller y agregar al init
    ## agregar schema de environment al dto
    ## Recorrer array de servicios
    ## Si hay dto crear el schema del dto
    ## crear funcion en el service class y verificar tipo de servicio
    

    # createController(name=name, path=path)
    # createDTO(name=name, path=path)
    # createService(name=name, path=path)

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