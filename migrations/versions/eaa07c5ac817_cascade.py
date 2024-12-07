"""cascade

Revision ID: eaa07c5ac817
Revises: c9ed45a94e00
Create Date: 2024-12-07 19:10:49.847520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'eaa07c5ac817'
down_revision: Union[str, None] = 'c9ed45a94e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'create_at',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.drop_constraint('comment_ibfk_2', 'comment', type_='foreignkey')
    op.drop_constraint('comment_ibfk_3', 'comment', type_='foreignkey')
    op.drop_constraint('comment_ibfk_1', 'comment', type_='foreignkey')
    op.create_foreign_key(None, 'comment', 'post', ['postID'], ['postID'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comment', 'comment', ['parentcommentID'], ['commentID'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comment', 'user', ['userID'], ['userID'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_foreign_key('comment_ibfk_1', 'comment', 'comment', ['parentcommentID'], ['commentID'])
    op.create_foreign_key('comment_ibfk_3', 'comment', 'user', ['userID'], ['userID'])
    op.create_foreign_key('comment_ibfk_2', 'comment', 'post', ['postID'], ['postID'])
    op.alter_column('comment', 'create_at',
               existing_type=sa.DateTime(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
