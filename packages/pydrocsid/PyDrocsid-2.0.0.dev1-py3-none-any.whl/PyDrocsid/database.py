from asyncio import BoundedSemaphore
from typing import TypeVar, Optional, Union, Iterable, Type, List

from sqlalchemy import create_engine

# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Query, Session

from PyDrocsid.async_thread import run_in_thread
from PyDrocsid.environment import DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD
from PyDrocsid.logger import get_logger

T = TypeVar("T")


logger = get_logger(__name__)


class DB:
    def __init__(self, hostname, port, database, username, password):
        self.engine: Engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4",
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20,
        )

        self._SessionFactory: sessionmaker = sessionmaker(bind=self.engine, expire_on_commit=False)
        self._Session = scoped_session(self._SessionFactory)
        self.Base: DeclarativeMeta = declarative_base()

        self.thread_semaphore = BoundedSemaphore(5)

    def create_tables(self):
        logger.debug("creating tables")
        self.Base.metadata.create_all(bind=self.engine)

    def close(self):
        self._Session.remove()

    def add(self, obj: T):
        self.session.add(obj)

    def delete(self, obj: T):
        self.session.delete(obj)

    def query(self, model: Type[T], **kwargs) -> Union[Query, Iterable[T]]:
        return self.session.query(model).filter_by(**kwargs)

    def all(self, model: Type[T], **kwargs) -> List[T]:
        return self.query(model, **kwargs).all()

    def first(self, model: Type[T], **kwargs) -> Optional[T]:
        return self.query(model, **kwargs).first()

    def count(self, model: Type[T], **kwargs) -> int:
        return self.query(model, **kwargs).count()

    def get(self, model: Type[T], primary_key) -> Optional[T]:
        return self.session.query(model).get(primary_key)

    @property
    def session(self) -> Session:
        return self._Session()


async def db_thread(function, *args, **kwargs):
    async with db.thread_semaphore:

        def inner():
            try:
                out = function(*args, **kwargs)
                db.session.commit()
            finally:
                db.close()
            return out

        return await run_in_thread(inner)


db = DB(
    hostname=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
    username=DB_USERNAME,
    password=DB_PASSWORD,
)
