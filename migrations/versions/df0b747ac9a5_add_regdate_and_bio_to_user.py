"""Add regdate and bio to user

Revision ID: df0b747ac9a5
Revises: bb16fb367f9c
Create Date: 2019-01-10 13:46:19.422109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df0b747ac9a5'
down_revision = 'bb16fb367f9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('regdate', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_regdate'), 'user', ['regdate'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_regdate'), table_name='user')
    op.drop_column('user', 'regdate')
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###