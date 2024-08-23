from sqlalchemy import Column, String, ForeignKey, Integer, create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os


database = f"mysql://root:{os.environ['mydb']}@localhost/farmed"
Base = declarative_base()

engine = create_engine(database)

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    email = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(100))
    date_joined = Column(String(20))

    def __init__(self, user_name, email, user_password, date_joined):
        self.user_name = user_name
        self.email = email
        self.user_password = user_password
        self.date_joined = date_joined


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    date_posted = Column(
        String(50), default=datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"))
    post = Column(String(2000))
    user_id = Column(Integer, ForeignKey("user_details.id"))
    category = Column(String(50))
    likes = Column(Integer, default=0)
    myfile = Column(String(200))

    def __init__(self, title, user_id, category, post, myfile):
        self.post = post
        self.category = category
        self.myfile = myfile
        self.user_id = user_id
        self.title = title


class Reply(Base):
    __tablename__ = "reply"
    id = Column(Integer, primary_key=True)
    reply = Column(String(1000))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("user_details.id"))

    def __init__(self, reply, post_id, user_id):
        self.post_id = post_id
        self.reply = reply
        self.user_id = user_id


Base.metadata.create_all(engine)
