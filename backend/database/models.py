import sys
sys.path.append("..")

from sqlalchemy.sql.schema import ForeignKey
from database.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class DbQuestion(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    question = Column(String)
    answer = Column(String)
