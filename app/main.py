from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.core.db import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="Botfarm users service")
    Base.metadata.create_all(bind=engine)

    @app.get("/health", tags=["service"])
    def healthcheck():
        return {"status": "ok"}

    app.include_router(users_router, prefix="/api/v1")
    return app


app = create_app()
