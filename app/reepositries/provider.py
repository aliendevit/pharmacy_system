from fastapi import Depends
from app.core.settings import settings

# SQLite imports
from sqlmodel import Session
from app.db.session_sqlite import get_session
from app.reepositries.medicines_sql import MedicinesRepoSQL
from app.reepositries.sales_sql import SalesRepoSQL

# Mongo imports
from app.db.session_mongo import get_db as get_mongo_db
from app.reepositries.medicines_mongo import MedicinesRepoMongo
from app.reepositries.sales_mongo import SalesRepoMongo

# Medicines repo provider
if settings.DB_BACKEND == "mongo":
    def get_medicines_repo(db = Depends(get_mongo_db)):
        return MedicinesRepoMongo(db)
else:
    def get_medicines_repo(session: Session = Depends(get_session)):
        return MedicinesRepoSQL(session)

# Sales repo provider
if settings.DB_BACKEND == "mongo":
    def get_sales_repo(db = Depends(get_mongo_db)):
        return SalesRepoMongo(db)
else:
    def get_sales_repo(session: Session = Depends(get_session)):
        return SalesRepoSQL(session)
