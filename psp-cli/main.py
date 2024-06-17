import click

from modules import createController, createDTO, createService

@click.group()
def cli():
    pass


def createModule(name: str, path: str):
    createController(name=name, path=path)
    createService(name=name, path=path)
    createDTO(name=name, path=path)


@cli.command()
@click.option('-mo', '--module', "module", default=None, help="Create a complete module")
@click.argument('path')
def generate(module, path):
    if module:
        createModule(name=module, path=path)
    else:
        click.echo(f"Error, put a name and a path correctly")


if __name__ == '__main__':
    cli()