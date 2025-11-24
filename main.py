from fastapi import FastAPI

app = FastAPI(title="Botfarm demo")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Botfarm is alive"}


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}
