from fastapi import FastAPI

app = FastAPI()


@app.get("/mi-recurso")
def read_root():
    return {"mensaje": "¡Hola, mundo!"}
