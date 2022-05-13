from db.tables import orm_context, app, web
from urls import urls


if __name__ == "__main__":
    app.add_routes(urls)
    app.cleanup_ctx.append(orm_context)

    web.run_app(app)
