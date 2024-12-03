"""user_todo_tables

Revision ID: 01ab5a8becde
Revises: 8b8227e2e67a
Create Date: 2024-12-03 16:02:18.665978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01ab5a8becde'
down_revision: Union[str, None] = '8b8227e2e67a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('userID', sa.String(), nullable=False),
    sa.Column('followID', sa.String(), nullable=False),
    sa.Column('follow_at', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['followID'], ['user.userID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('userID', 'followID')
    )
    op.create_index(op.f('ix_follow_followID'), 'follow', ['followID'], unique=False)
    op.create_index(op.f('ix_follow_userID'), 'follow', ['userID'], unique=False)
    op.create_table('post',
    sa.Column('postID', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('count_likes', sa.Integer(), nullable=True),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.String(length=255), nullable=True),
    sa.Column('update_at', sa.String(length=255), nullable=True),
    sa.Column('categoryname', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('postID')
    )
    op.create_index(op.f('ix_post_postID'), 'post', ['postID'], unique=False)
    op.create_table('comment',
    sa.Column('commentID', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('postID', sa.Integer(), nullable=True),
    sa.Column('parentcommentID', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['parentcommentID'], ['comment.commentID'], ),
    sa.ForeignKeyConstraint(['postID'], ['post.postID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('commentID')
    )
    op.create_index(op.f('ix_comment_commentID'), 'comment', ['commentID'], unique=False)
    op.create_table('like',
    sa.Column('userID', sa.String(), nullable=False),
    sa.Column('postID', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['postID'], ['post.postID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('userID', 'postID')
    )
    op.create_index(op.f('ix_like_postID'), 'like', ['postID'], unique=False)
    op.create_index(op.f('ix_like_userID'), 'like', ['userID'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_like_userID'), table_name='like')
    op.drop_index(op.f('ix_like_postID'), table_name='like')
    op.drop_table('like')
    op.drop_index(op.f('ix_comment_commentID'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_post_postID'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_follow_userID'), table_name='follow')
    op.drop_index(op.f('ix_follow_followID'), table_name='follow')
    op.drop_table('follow')
    # ### end Alembic commands ###
