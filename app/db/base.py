from sqlmodel import SQLModel
from app.models.medicine import Medicine
from app.models.sale import Sale

models = (Medicine, Sale)

def create_all(engine):
    SQLModel.metadata.create_all(engine)
