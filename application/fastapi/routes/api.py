from fastapi import UploadFile, File, Request, HTTPException
import dataset

from application.fastapi.classes.table import Table
from application.fastapi.classes.row import Row

db = dataset.connect("postgresql://postgres:123456@localhost:5432")

def init_app(app, access_point="/api", encoding='utf-8'):
    @app.get(access_point+"/{table}", tags=[access_point])
    async def get_table_itens(table, request: Request):
        return list(db[table].all()) if db[table] else {"error":"database not created"}

    @app.post(access_point+"/upload_file", tags=[access_point])
    async def post_file(file: UploadFile = File(...)):
        """all elements on a table"""
        lines = file.file.readlines()
        file_name = file.filename.split(".")[0]
        result, table_repository = await lines_to_object_list(file_name, lines)
        return_mensage = {"success": True}
        try:
            table_repository.insert_many([ob.__dict__ for ob in result])
        except Exception as e:
            raise HTTPException(status_code=409, detail={
                "success": False,
                 "error": str(e),
                "type": "Conflict"
            })
        return return_mensage
        #return result

    async def lines_to_object_list(file_name, lines):
        db = dataset.connect("postgresql://postgres:123456@localhost:5432")
        counter = 0
        result = []
        for i in lines:
            if counter == 0:
                table = Table(i.decode(encoding).split())
                if not db[file_name]:
                    table_repository = db.create_table(file_name,
                                                       primary_id='id',
                                                       primary_type=db.types.integer)
                    table_repository.create_column('cpf', db.types.string(20)) #unique=True, nullable=False)
                    table_repository.create_column('private', db.types.integer)
                    table_repository.create_column('incomplete', db.types.integer)
                    table_repository.create_column('date_last_buy', db.types.string(10))
                    table_repository.create_column('ticket_avg', db.types.string(8))
                    table_repository.create_column('ticket_last_buy', db.types.string(8))
                    table_repository.create_column('store_frequent', db.types.string)
                    table_repository.create_column('store_last', db.types.string)
                    table_repository.create_column('cpf_valid', db.types.boolean)
                    table_repository.create_column('cnpj_valid_store_frequent', db.types.boolean)
                    table_repository.create_column('store_last', db.types.boolean)

                    db.commit()
                else:
                    table_repository = db[file_name]
            else:
                item = Row(counter, i.decode(encoding).split(), table.fields)
                # table_repository.insert(item.__dict__)
                result.append(item)
            counter += 1
        return result, table_repository

    return app
