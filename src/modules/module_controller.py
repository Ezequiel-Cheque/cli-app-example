import click
from pathlib import Path


def createController(name: str, path: str):
    
    DIRNAME = f"{path}/src/psp/controller/{name}/"
    FILENAME = f"{path}/src/psp/controller/{name}/{name}_controller.py"

    dtoSchema = f"{name.lower()}TransactionSchema"
    dtoInput = f"{name.lower()}TransactionInput"
    service = f"{name[0].upper()}{name[1:]}Service"
    
    directoryPath = Path(DIRNAME)
    filePath = Path(FILENAME)
    
    directory = directoryPath.resolve()
    file = filePath.resolve()

    if not directory.exists():
        directoryPath.mkdir()
        click.echo("Directory controller created")
    
    if file.exists():
        click.echo("Controller existed")
    else:
        controllerCode = f"""
from fastapi import APIRouter, Request
from fastapi.security import HTTPBearer

from ...decoration import logs
from ...dto import {dtoSchema}, {dtoInput}
from ...service.{name}.{name}_service import {service}

{name} = APIRouter(prefix="/{name}", tags=["{name} psp integration"])
security = HTTPBearer()


@{name}.get("/form", description="Obtener formulario de pago", responses={{}})
async def form():
    return {dtoInput}().form()


@{name}.post("/create/transaction", description="Crear transaccion", responses={{}})
@logs
async def create(_: Request, body: {dtoSchema}):
    body = {dtoInput}.create(body)
    return await {service}(_).createTransaction(body)

    
@{name}.post("/get/status/{{id}}", description="Obtener status de la transaccion", responses={{}})
@logs
async def getStatus(_: Request, id: str, page: str = None):
    if page:
        _.page = page
    return {service}(_).getStatus(id)


@{name}.post("/webhook", description="Webhook", responses={{}})
@logs
async def form(_: Request, body: dict):
    return {service}(_).webhook(body)
        
"""
        f = open(filePath, "a")
        f.write(controllerCode)
        f.close()
        click.echo("Controller created")