import click
from pathlib import Path

@click.group()
def cli():
    pass

def createDTO(dto):
    FILENAME = f"src/psp/dto/input/create_transaction_{dto}_dto.py"

    filePath = Path(FILENAME)
    
    file = filePath.resolve()

    if file.exists():
        click.echo("dto existed")
    else:
        dtoCode = f"""
import json

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field

enum_currency = {{
    "MX": [{{"label": "MXN"}}],
    "PE": [{{"label": "USD"}}],
    "CL": [{{"label": "USD"}}],
    "CR": [{{"label": "USD"}}],
    "PA": [{{"label": "USD"}}],
    "BR": [{{"label": "USD"}}],
    "SV": [{{"label": "USD"}}],
    "GT": [{{"label": "USD"}}],
    "EC": [{{"label": "USD"}}],
    "UY": [{{"label": "USD"}}]
}}

class {dto.lower()}TransactionSchema(BaseModel):
    amount: int = Field(description="")
    currency: str = Field(description="")
    firstname: str = Field(description="")
    lastname: str = Field(description="")
    email: EmailStr = Field(description="")
    phone: str = Field(description="", min_length=8, max_length=10, example="5555555555")
    code: str = Field(description="")
    external_transaction_id: str = Field(description="")

class {dto.lower()}TransactionRoot(BaseModel):
    __root__: {dto.lower()}TransactionSchema

class {dto.lower()}TransactionInput:
    def create(createTransaction: {dto.lower()}TransactionSchema):
        jsonable_encoder({dto.lower()}TransactionRoot(__root__=createTransaction))
        non_empty_fields = {{field: value for field, value in createTransaction.dict().items() if value is not None}}
        return non_empty_fields

    def form():
        schema_dict = json.loads(clipTransactionSchema.schema_json())["properties"]

        for item in schema_dict.keys():
            schema_dict[item]["hiden"] = False
            schema_dict[item]["required"] = True

            if str(item) == "external_transaction_id":
                schema_dict[item]["hiden"] = True
                schema_dict[item]["required"] = False

            if str(item) == "email":
                schema_dict[item]["hiden"] = True
                schema_dict[item]["required"] = False

            if str(item) == "currency":
                schema_dict[item]["format"] = "super_select"
                schema_dict[item]["to"] = "country"
                schema_dict[item]["enum"] = enum_currency
                schema_dict[item]["hiden"] = False
                schema_dict[item]["required"] = True
                
            if str(item) == "firstname":
                schema_dict[item]["minLength"] = 3
                schema_dict[item]["maxLength"] = 20
                
            if str(item) == "lastname":
                schema_dict[item]["minLength"] = 3
                schema_dict[item]["maxLength"] = 20

            if str(item) == "code":
                schema_dict[item]["hiden"] = True
                schema_dict[item]["required"] = False
    
            if str(item) == "phone":
                schema_dict[item]["hiden"] = True
                schema_dict[item]["required"] = False

        return schema_dict

class {dto.lower()}ConfigurationSchema(BaseModel):
    baseapi: str = Field(description="")
    apikey: str = Field(description="")
    secretKey: str = Field(description="")

class {dto.lower()}ConfigurationRoot(BaseModel):
    __root___: {dto.lower()}ConfigurationSchema

class {dto.lower()}ConfigurationInput(BaseModel):
    def create(createInput: {dto.lower()}ConfigurationSchema):
        jsonable_encoder({dto.lower()}ConfigurationRoot(__root__=createInput))
        non_empty_fields = {{field: value for field, value in createInput.dict().items() if value is not None}}
        return non_empty_fields
        """
    f = open(filePath, "a")
    f.write(dtoCode)
    f.close()
    click.echo("DTO created")

def createService(service: str):
    DIRNAME = f"src/psp/service/{service}/"
    FILENAME = f"src/psp/service/{service}/{service}_service.py"

    directoryPath = Path(DIRNAME)
    filePath = Path(FILENAME)
    
    directory = directoryPath.resolve()
    file = filePath.resolve()

    if not directory.exists():
        directoryPath.mkdir()
        click.echo("Directory service created")
    
    if file.exists():
        click.echo("service existed")
    else:
        serviceCode = f"""
import json
import logging

from os import getenv
from ...util.request import Request
from ...util.enviroments import Enviroments
from ...util.validate_propeties import validate

class {service[0].upper()}{service[1:]}
    def __init__(self, _: Request):
        self.context = _
        self.requests = Request(self.context)
        
    def return_error(self, message="", providerId=None, res={{}}):
        response = {{}}
        response["success"] = False
        response["message"] = message
        response["type"] = "internal"
        response["autoApproved"] = False
        response["provider_id"] = providerId
        response["url"] = ""
        response["log"] = validate(self.context, "logId") and self.context.logId or ""
        response["payload"] = res

        return response
    
    async def createTransaction(self, body: dict):
        pass
    
    async def getStatus(self, idTransaction: str):
        pass
    
    async def webhook(self):
        pass
        
        """
        f = open(filePath, "a")
        f.write(serviceCode)
        f.close()
        click.echo("Service created")


def createController(name: str):
    DIRNAME = f"src/psp/controller/{name}/"
    FILENAME = f"src/psp/controller/{name}/{name}_controller.py"

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

{name} = APIRouter(prefix="/{name}", tags=["{name} psp integration"])
security = HTTPBearer()

@{name}.get("/form", description="Obtener formulario de pago", responses="")
async def form():
    pass

@{name}.post("/create/transaction", description="Crear transaccion", responses="")
async def form():
    pass
    
@{name}.post("/get/status", description="Obtener status de la transaccion", responses="")
async def form():
    pass

@{name}.post("/webhook", description="Webhook", responses="")
async def form():
    pass
        """
        f = open(filePath, "a")
        f.write(controllerCode)
        f.close()
        click.echo("Controller created")



def createModule(name):
    createController(name)
    createService(name)
    createDTO(name)


@cli.command()
@click.option('-co', '--controller', "controller", default=None, help="Create a controller")
@click.option('-s', '--service', "service", default=None, help="Create a service")
@click.option('-d', '--dto', "dto", default=None, help="Create an input dto")
@click.option('-mo', '--module', "module", default=None, help="Create a complete module")
def generate(controller, service, dto, module):
    if controller:
        createController(controller)
    if service:
        createService(service)
    if dto:
        createDTO(dto)
    if module:
        createModule(module)


if __name__ == '__main__':
    cli()