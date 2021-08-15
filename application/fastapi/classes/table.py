"""represent attributes of the table"""
class Table():
    """initialize table attributes"""
    def __init__(self, string, fields=["cpf",
                                        "private",
                                        "incomplete",
                                        "date_last_buy",
                                        "ticket_avg",
                                        "ticket_last_buy",
                                        "store_frequent",
                                        "store_last"]):
        self.fields = fields

    def table_definition(self, file_name, db):
        #define table attributes
        table = db.create_table(file_name,
                          primary_id='id',
                          primary_type=db.types.integer)
        #the column definition are optional and was being use to try reduce database size
        table.create_column('cpf', db.types.string(20))  # unique=True, nullable=False)
        table.create_column('private', db.types.integer)
        table.create_column('incomplete', db.types.integer)
        table.create_column('date_last_buy', db.types.string(10))
        table.create_column('ticket_avg', db.types.string(8))
        table.create_column('ticket_last_buy', db.types.string(8))
        table.create_column('store_frequent', db.types.string)
        table.create_column('store_last', db.types.string)
        table.create_column('cpf_valid', db.types.boolean)
        table.create_column('cnpj_valid_store_frequent', db.types.boolean)
        table.create_column('store_last', db.types.boolean)
        return table
