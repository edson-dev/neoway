from flask import Flask, request
import json
import abc
from unidecode import unidecode
from brutils import cpf, cnpj


app = Flask(__name__)
encoding = 'utf-8'

"""Represent each row in the table"""
class Row():
    def __init__(self, id, string, table):
        #initialize attributes using ones of the table
        self.id = id
        for label, item in zip(table, string):
            self.set_value(label, item)
            self.validador(label)

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

@app.route('/file_upload',methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    lines = uploaded_file.stream.readlines()
    c = 0
    result = []
    for i in lines:
        if(c == 0):
            table = Table(i.decode(encoding).split())
        else:
            item = Row(c, i.decode(encoding).split(), table.fields)
            result.append(item)
        c += 1

    return json.dumps([ob.__dict__ for ob in result])

if __name__ == '__main__':
    app.run()
