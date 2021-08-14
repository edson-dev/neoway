def init_app(app, access_point="/api"):


    @app.get(access_point, tags=[access_point])
    async def get():
        """all elements on a table"""
        return "test"

    return app
