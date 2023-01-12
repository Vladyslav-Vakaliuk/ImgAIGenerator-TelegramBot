import asyncio
import logging

from sqlalchemy import Column, String, MetaData, ForeignKey 
from sqlalchemy import Integer, DateTime, BIGINT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker, selectinload, relationship

from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

db_driver = 'postgresql+asyncpg'
db_user = env.str("DB_USER")
db_password = env.str("PG_PASSWORD")
db_host = env.str("DB_HOST")
db_port = env.str("PORT")
db_name = env.str("DB_NAME")

db_string = f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" # setting for connecting to database 

Base = declarative_base()

class User(Base): # Init table "users" 
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

    def __repr__(self):
        return f"User{(self.user_id, self.user_name, self.user_surname, self.username, self.language_code)}"

class Prompt(Base): # Init table "prompts"
    __tablename__ = "prompts"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", BIGINT)
    username = Column("username", String(100))
    prompt = Column("prompt", String)
    img_name = Column("img_name", String)

    def __init__(self, user_id, username, prompt, img_name):
        self.user_id = user_id
        self.username = username
        self.prompt = prompt
        self.img_name = img_name

    def __repl__(self):
        return f"From:{self.username}, prompt:{self.prompt}"

class Feedback(Base): # Init table "feedback"
    __tablename__ = "feedback"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", BIGINT)
    username = Column("username", String(100))
    review = Column("review", String)

    def __init__(self, user_id, username, review):
        self.user_id = user_id
        self.username = username
        self.review = review

    def __repl__(self):
        return f"From:{self.username}, review:{self.review}"

async def async_main():
    global SessionMaker, engine
    try:
        engine = create_async_engine(db_string, echo=False) 

        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all) # delete all tables when bot started
            await conn.run_sync(Base.metadata.create_all) # create all tables when bot started 

        SessionMaker = sessionmaker(engine,
                                    expire_on_commit=False, 
                                    class_=AsyncSession)

        await engine.dispose()
    except:
        logger.info("Got problems with database")
        pass

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(async_main())

class Database:
    """Add user to database"""
    async def add_user_to_db(user_id: int, user_name: str, user_surname: str, username: str, language: str):
        user = User(user_id=user_id, name=user_name, surname=user_surname, username=username, language=language)
        async with SessionMaker.begin() as session: 
            session.add(user)
            await session.commit()
            logger.info(f"Added new user to database, user_id {user.user_id}")

    """Checking whether the user is in the database"""
    async def chek_user_in_db(user_id: int):
        async with SessionMaker.begin() as session:
            statement = select(User).where(User.user_id == user_id)
            result = await session.execute(statement)
            curr = result.scalars()

            for user in curr:
                return True

            await engine.dispose()
    
    """Get all user id from database"""
    async def get_all_user_id():
        async with SessionMaker.begin() as session:
            result = await session.execute(select(User.user_id).order_by(User.user_id))
            return result.scalars()

    """Save user response(prompt)"""
    async def save_prompt_to_database(user_id: int, username: str, prompt: str, img_name: str):
        prompt = Prompt(user_id=user_id, username=username, prompt=prompt, img_name=img_name)
        async with SessionMaker.begin() as session:
            session.add(prompt)
            await session.commit()

    """Save the user's feedback in the database"""
    async def save_feedback(user_id: int, username: str, review: str):
        feedback = Feedback(user_id=user_id, username=username, review=review)
        async with SessionMaker.begin() as session:
            session.add(feedback)
            await session.commit()
            logger.info(f"User: {username}, added review: {review}")