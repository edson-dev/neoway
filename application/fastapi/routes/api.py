from fastapi import UploadFile, File
import dataset

from application.fastapi.classes.table import Table
from application.fastapi.classes.row import Row

def init_app(app, access_point="/api", encoding='utf-8'):
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
        counter = 0
        result = []
        for i in lines:
            if counter == 0:
                table = Table(i.decode(encoding).split())
                if not db[file_name]:
                    table_repository = db.create_table(file_name,
                                            primary_id='id',
                                            primary_type=db.types.integer)
                    db.commit()
                else:
                    table_repository = db[file_name]
            else:
                item = Row(counter, i.decode(encoding).split(), table.fields)
                #table_repository.insert(item.__dict__)
                result.append(item)
            counter += 1
        r = {"success": True}
        try:
            table_repository.insert_many([ob.__dict__ for ob in result])
        except Exception as e:
            r = {"success": False,
                 "error": str(e)}

        return r
        #return result

    return app
