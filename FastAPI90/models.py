from sqlalchemy import text, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey  # must import
from sqlalchemy.orm import relationship

# to create a
# column,import integer,

from FastAPI90.database import Base #defines out models

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default = "True", nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text("now()"))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False)

    owner = relationship("User")#fetches user based on their owner_id

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    email=Column (String(255), nullable = False,unique = True)
    password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text("now()"))
    phone_num = Column(String(20),nullable =True,unique=True)

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,)
