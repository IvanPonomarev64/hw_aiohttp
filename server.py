from db.tables import orm_context
from urls import *


if __name__ == "__main__":
    app.cleanup_ctx.append(orm_context)

    web.run_app(app)
