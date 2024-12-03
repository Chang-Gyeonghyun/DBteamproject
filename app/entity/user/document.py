from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "user"
    userID = Column(String(255), primary_key=True, index=True)
    email = Column(String(255))
    hashed_password = Column(String(255))
    phone = Column(String(255))
    gender = Column(String(255))
    birth = Column(String(255))
    name = Column(String(255))
    nickname = Column(String(255))
    profile_image = Column(String(255))
    
    likes = relationship("Like", back_populates="user", lazy="joined")
    follow = relationship("follow", back_populates="user")