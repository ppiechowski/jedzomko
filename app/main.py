from fastapi import FastAPI
from app.database import Base, engine
from app.routes import entries, barcode

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jedzomko API")

app.include_router(entries.router)
app.include_router(barcode.router)

@app.get("/")
def root():
    return {"message": "Jedzomko API działa"}