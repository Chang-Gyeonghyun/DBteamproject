from sqlalchemy import Column, ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

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
    introduce = Column(String(255))
    profile_image = Column(String(255))

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    following = relationship("Follow", foreign_keys="[Follow.userID]", back_populates="follower")
    followers = relationship("Follow", foreign_keys="[Follow.followID]", back_populates="followee")
    
class Post(Base):
    __tablename__ = "post"
    postID = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    count_likes = Column(Integer, default=0)
    userID = Column(String(255), ForeignKey("user.userID", ondelete="CASCADE"))
    create_at = Column(DateTime, default=datetime.now(timezone.utc))
    update_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="post", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="post", cascade="all, delete-orphan")
    
class Comment(Base):
    __tablename__ = "comment"
    commentID = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    userID = Column(String(255), ForeignKey("user.userID"))
    postID = Column(Integer, ForeignKey("post.postID"))
    parentcommentID = Column(Integer, ForeignKey("comment.commentID"))
    create_at = Column(String(255))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", back_populates="replies", remote_side=[commentID])
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")

class Follow(Base):
    __tablename__ = "follow"
    userID = Column(String(255), ForeignKey("user.userID", ondelete="CASCADE"), primary_key=True)
    followID = Column(String(255), ForeignKey("user.userID", ondelete="CASCADE"), primary_key=True)
    follow_at = Column(DateTime, default=datetime.now(timezone.utc))

    follower = relationship("User", foreign_keys=[userID], back_populates="following")
    followee = relationship("User", foreign_keys=[followID], back_populates="followers")

class Like(Base):
    __tablename__ = "like"
    userID = Column(String(255), ForeignKey("user.userID", ondelete="CASCADE"), primary_key=True)
    postID = Column(Integer, ForeignKey("post.postID", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    
class Keyword(Base):
    __tablename__ = "keyword"
    postID = Column(Integer, ForeignKey("post.postID", ondelete="CASCADE"), primary_key=True)
    name = Column(String(255), primary_key=True, nullable=False)

    posts = relationship("PostKeyword", back_populates="keyword", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = "attachment"
    attachmentID = Column(Integer, primary_key=True, index=True)
    postID = Column(Integer, ForeignKey("post.postID", ondelete="CASCADE"))
    fileName = Column(String(255), nullable=False)
    filePath = Column(String(255), nullable=False)

    post = relationship("Post", back_populates="attachments")