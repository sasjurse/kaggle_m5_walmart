import os

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from src.generics.postgres import import_secrets_from_local

"""NB. We are using sqlalchemy for doing inserts without worrying about SQL-injection attacks. However, note that
this library have massive speed issues in our code. 
"""
base = declarative_base()


class SearchTerm(base):
    __tablename__ = 'search_term'

    search_term = sa.Column(sa.String(140), primary_key=True)
    location = sa.Column(sa.String(140))


class Example(base):
    __tablename__ = 'examples'

    id = sa.Column(sa.types.BigInteger,  primary_key=True)
    text = sa.Column(sa.String(280))
    created_at = sa.Column(sa.types.DateTime)
    sentiment = sa.Column(sa.types.FLOAT)


def create_sa_engine():
    if not os.getenv('POSTGRES_SERVICE_HOST'):
        import_secrets_from_local()
    db_string = f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@" \
                f"{os.environ['POSTGRES_SERVICE_HOST']}:5432"

    return sa.create_engine(db_string)


def create_sa_session():
    return sa.orm.Session(create_sa_engine())
