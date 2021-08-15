from unidecode import unidecode
from brutils import cpf, cnpj


"""Represent each row in the table"""
class Row():
    """initialize each attribute of the table with one field of the line in the file"""
    def __init__(self, id_code, string, table):
        self.id = id_code
        for label, item in zip(table, string):
            self.set_value(label, item)
            self.validador(label)

    """if a attribute need a validation its trigger by the label name"""
    def validador(self, label):
        if label in ["cpf"]:
            self.cpf_valid = cpf.validate(cpf.sieve(self.cpf))
        if label in ["store_frequent"]:
            self.cnpj_valid_store_frequent = cnpj.validate(cnpj.sieve(self.store_frequent))
        if label in ["store_last"]:
            self.cnpj_valid_store_last = cnpj.validate(cnpj.sieve(self.store_last))

    """set attribute value buy string name"""
    def set_value(self, label, item):
        value = unidecode(item).lower()
        setattr(self, label, value)

    def to_string(self):
        ...
