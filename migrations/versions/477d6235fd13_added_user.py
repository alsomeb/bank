"""Added user

Revision ID: 477d6235fd13
Revises: 9fc247431831
Create Date: 2022-01-28 11:15:20.384408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '477d6235fd13'
down_revision = '9fc247431831'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('first_name', sa.String(length=100), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=100), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Employee')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Employee',
    sa.Column('Id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Email', mysql.VARCHAR(length=150), nullable=False),
    sa.Column('Password', mysql.VARCHAR(length=150), nullable=False),
    sa.Column('Role', mysql.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('Id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('user_roles')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
