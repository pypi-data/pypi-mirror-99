# Database
On the device we use `sqlalchemy` for our database. Additionally we use `alembic` for our migrations.
An example of a database is included in openmodule-test

## Models
### Definition
All database models inherit a `Base` from `sqlalchemy` and need an unique id.

```python
import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseTestModel(Base):
    __tablename__ = "test"
    id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, primary_key=True)
    value = Column(Integer, default=1)
    string = Column(String, default="initial")
```

### Registration
All database models you want to use need to registered. This happens in the `src/database/alembic/env.py` file. Simply list all used Bases in the register_bases function.
```python
from database.database_models import Base
from somewhere import Base as some_base
register_bases([Base, some_base])
```

## Migrations

### Generating migrations
To generate the migration use the provided script `src/database/makemigration.sh` with a name for your migration.
```shell script
./makemigrations -m <name>
```
Afterwards the migrations are created under `src/database/alembic/versions`.

### Migrating
The database is always automatically migrated on creation of any database in the program.


## Database Access

To access the database we have to create our own instance, you can also pass the parameter `database=True` to the core for it to create a database:
Then we can create a session an access the database.
```python
database = Database(**kwargs)
with database as db:
    do_stuff(db, ...)
```

If an exception is raised during an open database session, all changes will be rolled back.  
It is also possible to create multiple database within a program, but the need to is quite questionable.


## Basic db stuff 
Normally sqlalchemy functions should suffice for most jobs. We implemented some additional functionality as functions under `openmodule.utils.db_helper`. 

### create
* db.add(model: DatabaseModel)
* db.add_all(models: List[DatabaseModel])    
    
### query
* base_query = db.query(DatabaseModel)
* query = base_query..filter_by(**kwargs) 
* query.all() returns a list

### query single object
* instance = query.one() -> returns element or raises exception if query has more or no elements (MultipleResultsFound, NoResultFound)
* instance = query.first() -> returns first element of query or None

### update
* db.add(model: DatabaseModel) -> previously created model
* db_helper.update_query(db, query, values: dict)

### delete
* db.delete(model: DatabaseModel)
* db_helper.delete_query(db, query)


### Useful query stuff
* order_by(*args) -> ordering
* yield_by(int) -> for batch processing
* distinct(*args) -> distinct
