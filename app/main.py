from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, engine, false
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

connection_string = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\Voramet\Web applications\testAccess\app\Database1.accdb;"
    r"ExtendedAnsiSQL=1;"
)
connection_url = engine.URL.create(
    "access+pyodbc", query={"odbc_connect": connection_string}
)
engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    res = db.execute("SELECT * FROM table1")
    keys = [k for k in res.keys()]
    result = [dict(zip(keys, r)) for r in res]
    return result
