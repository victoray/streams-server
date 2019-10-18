from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)


class Stream(Base):
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    description = Column(String(2500), nullable=False)
    user_id = Column(String(250), ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'userId': self.user_id
        }


engine = create_engine('sqlite:///streams.db')

Base.metadata.create_all(engine)
