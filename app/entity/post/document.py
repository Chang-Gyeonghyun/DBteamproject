from sqlalchemy import Column, ForeignKey, String, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "post"
    postID = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    count_likes = Column(Integer, default=0)
    userID = Column(Integer, ForeignKey("user.id"))
    create_at = Column(String(255))
    update_at = Column(String(255))
    categoryname = Column(String(255))
    
    user = relationship("User", back_populates="post")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")