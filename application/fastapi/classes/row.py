from unidecode import unidecode
from brutils import cpf, cnpj

class Row():
    def __init__(self, id_code, string, table):
        self.id = id_code
        for label, item in zip(table, string):
            self.set_value(label, item)
            self.validador(label)

    def validador(self, label):
        if label in ["cpf"]:
            self.cpf_valid = cpf.validate(cpf.sieve(self.cpf))
        if label in ["store_frequent"]:
            self.cnpj_valid_store_frequent = cnpj.validate(cnpj.sieve(self.store_frequent))
        if label in ["store_last"]:
            self.cnpj_valid_store_last = cnpj.validate(cnpj.sieve(self.store_last))

    def set_value(self, label, item):
        value = unidecode(item).lower()
        setattr(self, label, value)

    def to_string(self):
        ...
