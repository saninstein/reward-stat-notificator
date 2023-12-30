from sqlalchemy.orm import declarative_base


class Model(declarative_base()):
    __abstract__ = True
