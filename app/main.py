import uuid
from datetime import datetime
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, Field


class Record(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime | None = Field(default_factory=datetime.now)
    weight: float = Field(default=0.0)


# Postgres connection string
DATABASE_URL = "postgresql+psycopg://go:green@localhost:5432/compose"
engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
SQLModel.metadata.create_all(engine)


# Create a session
def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/records")
async def get_records():
    with Session(engine) as session:
        records = (
            session.query(Record).order_by(Record.timestamp.desc()).limit(100).all()
        )
        return records


@app.get("/records/{record_id}")
async def get_record(record_id: uuid.UUID):
    with Session(engine) as session:
        record = session.query(Record).filter(Record.id == record_id).first()
        if record:
            return record
        else:
            return {"error": "Record not found"}


@app.post("/records")
async def create_record(record: Record):
    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


@app.put("/records/{record_id}")
async def update_record(record_id: uuid.UUID, weight: float):
    with Session(engine) as session:
        record = session.query(Record).filter(Record.id == record_id).first()
        if record:
            record.weight = weight
            session.commit()
            session.refresh(record)
            return record
        else:
            return {"error": "Record not found"}


@app.delete("/records/{record_id}")
async def delete_record(record_id: uuid.UUID):
    with Session(engine) as session:
        record = session.query(Record).filter(Record.id == record_id).first()
        if record:
            session.delete(record)
            session.commit()
            return {"message": "Record deleted"}
        else:
            return {"error": "Record not found"}
