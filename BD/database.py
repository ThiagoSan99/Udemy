import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'Movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseurl = f'sqlite:///{os.path.join(base_dir, sqliteName)}'

motor = create_engine(databaseurl, echo=True)

Session = sessionmaker(bind=motor)

Base = declarative_base()