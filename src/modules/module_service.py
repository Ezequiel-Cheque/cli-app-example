import click
from pathlib import Path


def createService(name: str, path: str):
    DIRNAME = f"{path}/src/psp/services/{name}/"
    FILENAME = f"{path}/src/psp/services/{name}/{name}_service.py"

    dtoSchema = f"{name.lower()}TransactionSchema"

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
from ...dto import {dtoSchema}

class {name[0].upper()}{name[1:]}Service:

    def __init__(self, _: Request):
        self.context = _
        self.requests = Request(self.context)
        self.webhook = getenv("PR_WEBHOOK")
    
        
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
    
    
    async def createTransaction(self, body: {dtoSchema}):
        enviroment = Enviroments.get_enviroment(self.context, self.context.psp, self.context.page)
        
        payload = {{}}
        
        return "Create a transaction"
    
    
    async def getStatus(self, idTransaction: str):
        enviroment = Enviroments.get_enviroment(self.context, self.context.psp, self.context.page)
        
        return "Show transaction status"
    
    
    async def webhook(self, body: dict):
        return "Get webhook successfully"
        
        """
        f = open(filePath, "a")
        f.write(serviceCode)
        f.close()
        click.echo("Service created")