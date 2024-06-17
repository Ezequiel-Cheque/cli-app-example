import click
from pathlib import Path


def createDTO(name, path: str):
    FILENAME = f"{path}/src/psp/dto/input/create_transaction_{name}_dto.py"

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

class {name.lower()}TransactionSchema(BaseModel):
    amount: int = Field(description="")
    currency: str = Field(description="")
    firstname: str = Field(description="")
    lastname: str = Field(description="")
    email: EmailStr = Field(description="")
    phone: str = Field(description="", min_length=8, max_length=10, example="5555555555")
    code: str = Field(description="")
    external_transaction_id: str = Field(description="")

class {name.lower()}TransactionRoot(BaseModel):
    __root__: {name.lower()}TransactionSchema

class {name.lower()}TransactionInput:
    def create(createTransaction: {name.lower()}TransactionSchema):
        jsonable_encoder({name.lower()}TransactionRoot(__root__=createTransaction))
        non_empty_fields = {{field: value for field, value in createTransaction.dict().items() if value is not None}}
        return non_empty_fields

    def form():
        schema_dict = json.loads({name.lower()}TransactionSchema.schema_json())["properties"]

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

class {name.lower()}ConfigurationSchema(BaseModel):
    baseapi: str = Field(description="")
    apikey: str = Field(description="")
    secretKey: str = Field(description="")

class {name.lower()}ConfigurationRoot(BaseModel):
    __root___: {name.lower()}ConfigurationSchema

class {name.lower()}ConfigurationInput(BaseModel):
    def create(createInput: {name.lower()}ConfigurationSchema):
        jsonable_encoder({name.lower()}ConfigurationRoot(__root__=createInput))
        non_empty_fields = {{field: value for field, value in createInput.dict().items() if value is not None}}
        return non_empty_fields
"""
    f = open(filePath, "a")
    f.write(dtoCode)
    f.close()
    click.echo("DTO created")