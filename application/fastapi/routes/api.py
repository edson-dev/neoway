import json

from fastapi import UploadFile,File
from sqlalchemy.sql import text
from unidecode import unidecode
from brutils import cpf, cnpj
import dataset

encoding = 'utf-8'

class Row():
    def __init__(self, id, string, table):
        self.id = id
        for label, item in zip(table, string):
            self.set_value(label, item)
            self.validador(label)
        # self.id = id
        # document = CPF(string[0])
        # self.cpf = document.value
        # self.cpf_valid = document.valid
        # self.private = string[1]
        # self.incomplete = string[2]
        # self.last_buy_date = string[3]
        # self.ticket = string[4]
        # self.ticket_last_buy = string[5]
        # self.shop = string[6]
        # self.shop_last = string[7]
        # print(f"Row:{self.__dict__}")

    def validador(self, label):
        if label in ["cpf"]:
            self.cpf_valid = cpf.validate( cpf.sieve(self.cpf))
        if label in ["shop"]:
            self.cnpj_valid = cnpj.validate(cnpj.sieve(self.shop))

    def set_value(self, label, item):
        value = unidecode(item).lower()
        setattr(self, label, value)

    def to_string(self):
        ...


class Table():
    def __init__(self, string,default = ["cpf", "private", "incomplete", "last_buy_date", "ticket", "ticket_last_buy", "shop", "shop_last"]):
        self.fields = default
        print(f"Table:{self.__dict__}")

    def to_string(self):
        ...

def init_app(app, access_point="/api"):
    @app.get(access_point, tags=[access_point])
    async def get():
        """all elements on a table"""
        return "test"

    @app.post(access_point+"/upload_file", tags=[access_point])
    async def post_file(file: UploadFile = File(...)):
        """all elements on a table"""
        db = dataset.connect("postgresql://postgres:123456@localhost:5432")
        lines = file.file.readlines()
        file_name = file.filename.split(".")[0]
        c = 0
        result = []
        for i in lines:
            if (c == 0):
                table = Table(i.decode(encoding).split())
                if not db[file_name]:
                    database_table = db.create_table(file_name,
                                            primary_id='id',
                                            primary_type=db.types.integer)
                    db.commit()
                else:
                    database_table = db[file_name]
            else:
                item = Row(c, i.decode(encoding).split(), table.fields)
                #database_table.insert(item.__dict__)
                result.append(item)
            c += 1
        database_table.insert_many([ob.__dict__ for ob in result])

        return {"success":True}
        #return result

    return app
