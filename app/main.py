from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Botfarm")

    @app.get("/")
    def root():
        return {"status": "ok"}

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app


app = create_app()
