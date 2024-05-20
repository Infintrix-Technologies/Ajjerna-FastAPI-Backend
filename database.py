
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dependencies import return_db
from settings import settings
import datetime
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
engine = create_engine(settings.DATABASE_URI,
                    #    convert_unicode=True,
                       echo=False,
                       
                       # connect_args={"check_same_thread": False
                       #               }
                       )

SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


class TimeStampMixin:
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.datetime.utcnow)
    deleted_at = sa.Column(sa.DateTime)


class CRUD:

    db: Session = return_db()

    @classmethod
    def find(cls, **kwargs):

        if kwargs:

            instance = cls.db.query(cls).filter_by(**kwargs).first()

            if instance:
                return instance
            raise HTTPException(status_code=404, detail="Not Found")
        raise HTTPException(
            status_code=400, detail="Id or keyword argument missing following /")

    @classmethod
    def findAll(cls, *args, **kwargs):

        if kwargs:
            return cls.db.query(cls).filter_by(**kwargs).all()
        else:
            return cls.db.query(cls).all()

    @classmethod
    def findAllClass(cls, *args, **kwargs):

        if args:
            return cls.db.query(cls).filter(*args).all()
        elif kwargs:
            return cls.db.query(cls).filter(**kwargs).all()
        else:
            return cls.db.query(cls).all()

    def delete(self):

        self.db.delete(self)
        self.db.commit()
        raise HTTPException(status_code=200, detail=f"{self} Deleted")

    def update(self, *args, **kwargs):
        self.db.commit()
        return self.db.refresh(self)

    def update_dynamic(self, **kwargs):

        # print(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.db.commit()
        return self.db.refresh(self)

    def save(self, success_message="Created", commit=True):
        if commit:
            try:
                self.db.add(self)
                self.db.commit()

                self.db.refresh(self)

                raise HTTPException(
                    status_code=201, detail=success_message)

            except IntegrityError as err:
                self.db.rollback()
                raise HTTPException(status_code=409, detail="Already Exist")


class BaseModel(Base, CRUD):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
