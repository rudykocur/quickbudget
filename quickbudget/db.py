import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db(databaseUrl=None):

    if databaseUrl is None:
        with open('config.yaml') as f:
            config = yaml.load(f)

        databaseUrl = config['database']

    engine = create_engine(databaseUrl, convert_unicode=True)
    db_session.configure(bind=engine)

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #import yourapplication.models
    import quickbudget.schema
    
    #Base.metadata.create_all(bind=engine)