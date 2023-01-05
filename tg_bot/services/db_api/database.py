import asyncio
import logging

from sqlalchemy import Column, String, MetaData, ForeignKey
from sqlalchemy import Integer, DateTime, BIGINT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker, selectinload, relationship

from environs import Env

logging.basicConfig(filename="db_logs.log", level=logging.INFO)

env = Env()
env.read_env()

db_driver = 'postgresql+asyncpg'
db_user = env.str("DB_USER")
db_password = env.str("PG_PASSWORD")
db_host = env.str("DB_HOST")
db_port = env.str("PORT")
db_name = env.str("DB_NAME")

db_string = f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column("user_id", Integer, primary_key=True)
    user_name = Column("user_name", String(100))
    user_surname = Column("user_surname", String(100))
    username = Column("username", String(100))
    language_code = Column("language_code", String(100))


    def __init__(self, user_id, name, surname, username, language):
        self.user_id = user_id
        self.user_name = name
        self.user_surname = surname
        self.username = username
        self.language_code = language

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load

    def __repr__(self):
        return f"User{(self.user_id, self.user_name, self.user_surname, self.username, self.language_code)}"

async def async_main():
    global SessionMaker
    engine = create_async_engine(db_string, echo=False) 
    # return sqlalchemy.ext.asyncio.engine.AsyncEngine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    SessionMaker = sessionmaker(engine,
                            expire_on_commit=False, 
                            class_=AsyncSession)

    await engine.dispose()


asyncio.run(async_main())

async def add_user_to_db(user_id: int, user_name: str, user_surname: str, username: str, language: str):
    user = User(user_id=user_id, name=user_name, surname=user_surname, username=username, language=language)
    async with SessionMaker.begin() as session:  # return sqlalchemy.orm.session.AsyncSession
        session.add(user)
        await session.commit()

