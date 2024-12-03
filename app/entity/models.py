from sqlalchemy import Column, ForeignKey, String, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

# class Comment(Base):
#     __tablename__ = "comments"
#     commentID = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     create_datetime = Column(String(255))
#     user_id = Column(Integer, ForeignKey("user.userID"))
#     post_id = Column(Integer, ForeignKey("posts.postID"))
#     parent_id = Column(Integer, ForeignKey("comments.commentID"))
#     likes = Column(Integer, default=0)   
#     dislikes = Column(Integer, default=0)

#     user = relationship("User", back_populates="comments")
#     post = relationship("Post", back_populates="comments")
#     parent = relationship("Comment", back_populates="replies", remote_side=[id])
#     replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
#     likes_dislikes = relationship("UserLikeDislike", back_populates="comment", cascade="all, delete-orphan")
    
class Follow(Base):
    __tablename__ = "follow"
    userID = Column(String, ForeignKey("user.userID"), primary_key=True, index=True)
    followID = Column(String, ForeignKey("user.userID"), primary_key=True, index=True)
    follow_at = Column(String)

    user = relationship("User", back_populates="follow")
    
class Like(Base):
    __tablename__ = "like"
    userID = Column(String, ForeignKey("user.userID"), primary_key=True, index=True)
    postID = Column(String, ForeignKey("post.postID"), primary_key=True, index=True)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
