import os
import sys
import threading
import warnings
from typing import Optional

from alembic import command, context
from alembic.config import Config
from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def alembic_config(connection, alembic_path):
    alembic_cfg = Config(os.path.join(alembic_path, "alembic.ini"),
                         attributes={
                             "configure_logging": False,
                             "connection": connection,
                         })
    alembic_cfg.set_main_option("script_location", os.path.join(alembic_path, "alembic"))
    return alembic_cfg


def migrate_database(connection, alembic_path=None):
    if alembic_path is None:
        alembic_path = os.path.join(os.getcwd(), "database")
    assert os.path.exists(os.path.abspath(alembic_path)), f"alembic path {os.path.abspath(alembic_path)} does not exist"
    config = alembic_config(connection, alembic_path)
    command.upgrade(config, "head")


active_databases = {}


def register_bases(bases, show_deprecation_warning=True):
    if show_deprecation_warning:
        warnings.warn('\n\n`register_bases([...])` followed by `from openmodule.database.env import *` is deprecated.\n '
                      'Please replace these lines with `run_env_py([bases...])`\n',
                      DeprecationWarning)

    target_metadata = MetaData()

    if not isinstance(bases, list):
        bases = [bases]

    for base in bases:
        for table in base.metadata.tables.values():
            table.tometadata(target_metadata)

    context.config.attributes["target_metadata"] = target_metadata


def run_env_py(bases):
    register_bases(bases, show_deprecation_warning=False)
    # noinspection PyUnresolvedReferences
    import openmodule.database.env
    del sys.modules["openmodule.database.env"]


def database_path(db_folder, db_name):
    return os.path.join(db_folder, db_name) + ".sqlite3"


def get_database(db_folder: str, name: str, alembic_path=None):
    global active_databases
    tmp = database_path(db_folder, name)
    assert active_databases.get(tmp) is None, f"database {tmp} already exists," \
                                              f" check if it was shutdown before a new one was created"
    os.makedirs(db_folder, exist_ok=True)
    path = f"sqlite:///{tmp}"
    engine = create_engine(path, poolclass=StaticPool, connect_args={'check_same_thread': False})
    migrate_database(engine, alembic_path)
    active_databases[tmp] = engine
    return engine


class DatabaseContext:
    def __init__(self, database: 'Database', expire_on_commit=True):
        self.database = database
        self.expire_on_commit = expire_on_commit

    def __enter__(self) -> Session:
        return self.database.__enter__(expire_on_commit=self.expire_on_commit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.database.__exit__(exc_type, exc_val, exc_tb)


class Database:
    active_session: Optional[Session]

    def __init__(self, database_folder, name="database", alembic_path=None):
        self.db_folder = database_folder
        self.name = name
        self._engine = get_database(database_folder, name, alembic_path)
        self._session = sessionmaker(self._engine)
        self.active_session = None
        self.lock = threading.RLock()

    def is_open(self):
        return bool(self._session)

    def shutdown(self):
        assert self.is_open(), (
            "database is already closed, you called shutdown twice somewhere"
        )
        with self.lock:
            self._session = None
            global active_databases
            active_databases.pop(database_path(self.db_folder, self.name), None)

    def __call__(self, expire_on_commit=True) -> DatabaseContext:
        return DatabaseContext(self, expire_on_commit=expire_on_commit)

    def __enter__(self, expire_on_commit=True) -> Session:
        assert self._session, "Database is already closed"
        self.lock.acquire()
        self.active_session = self._session(expire_on_commit=expire_on_commit)
        return self.active_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.active_session.commit()
            else:
                self.active_session.rollback()
            self.active_session.close()
        except Exception as e:
            exc_type = exc_type or type(e)
        finally:
            self.active_session = None
            self.lock.release()
        return exc_type is None
