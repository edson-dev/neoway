from typing import Optional
from fastapi import UploadFile, File, Request, HTTPException
import dataset

from classes.row import Row
from classes.table import Table

#define the database connection o start
# use "localhost" or "postgres" when building docker
env = "localhost"
db = dataset.connect(f"postgresql://postgres:123456@{env}:5432")


#innit app is a factory pattern that avoid ciclyc importation of the app
#it split responsibility and use in that module only libs and services that it needs
def init_app(app, access_point="/api", encoding='utf-8'):


    #endpoint that recive the file upload
    @app.post(access_point+"/upload_file", tags=[access_point])
    async def post_file(file: UploadFile = File(...)):
        """all lines in the file"""
        if file.filename == "":
            return {"error": "empty file"}
        lines = file.file.readlines()
        #use filename w/o extesion for database name
        file_name = file.filename.split(".")[0]
        result, table_repository = await lines_to_object_list(file_name, lines)
        return_message = {"success": True}
        #presist objects to database as a single insert many and in dictionary format
        try:
            table_repository.insert_many([ob.__dict__ for ob in result])
        except Exception as e:
            raise HTTPException(status_code=409, detail={
                "success": False,
                 "error": str(e),
                "type": "Conflict"
            })
        return return_message

    # simple route that return all the itens on database as a json format
    ##todo optimize time with search restriction and cache usage since it's not change data
    @app.get(access_point + "/table/{table}", tags=[access_point])
    async def get_table_itens(table, request: Request):
        return list(db[table].all()) if db[table] else {"error": "database not created"}

    #transforma each line in a Row object
    async def lines_to_object_list(file_name, lines):
        #reset database connection to avoid change data before rea data
        db = dataset.connect(f"postgresql://postgres:123456@{env}:5432")
        counter = 0
        result = []
        for i in lines:
            if counter == 0:
                table = Table(i.decode(encoding).split())
                if not db[file_name]:
                    table_repository = table.table_definition(file_name, db)
                    db.commit()
                else:
                    table_repository = db[file_name]
            else:
                item = Row(counter, i.decode(encoding).split(), table.fields)
                # can try use insert one by one but time is a issue that way
                # table_repository.insert(item.__dict__)
                result.append(item)
            counter += 1
        return result, table_repository

    return app
