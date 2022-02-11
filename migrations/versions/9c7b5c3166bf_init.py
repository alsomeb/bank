"""init

Revision ID: 9c7b5c3166bf
Revises: 
Create Date: 2022-01-14 14:05:36.161793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7b5c3166bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Customers',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('GivenName', sa.String(length=50), nullable=False),
    sa.Column('Surname', sa.String(length=50), nullable=False),
    sa.Column('Streetaddress', sa.String(length=50), nullable=False),
    sa.Column('City', sa.String(length=50), nullable=False),
    sa.Column('Zipcode', sa.String(length=10), nullable=False),
    sa.Column('Country', sa.String(length=30), nullable=False),
    sa.Column('CountryCode', sa.String(length=2), nullable=False),
    sa.Column('Birthday', sa.DateTime(), nullable=False),
    sa.Column('NationalId', sa.String(length=20), nullable=False),
    sa.Column('TelephoneCountryCode', sa.Integer(), nullable=False),
    sa.Column('Telephone', sa.String(length=20), nullable=False),
    sa.Column('EmailAddress', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Accounts',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('AccountType', sa.String(length=10), nullable=False),
    sa.Column('Created', sa.DateTime(), nullable=False),
    sa.Column('Balance', sa.Integer(), nullable=False),
    sa.Column('CustomerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['CustomerId'], ['Customers.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Transactions',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Type', sa.String(length=20), nullable=False),
    sa.Column('Operation', sa.String(length=50), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('Amount', sa.Integer(), nullable=False),
    sa.Column('NewBalance', sa.Integer(), nullable=False),
    sa.Column('AccountId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['AccountId'], ['Accounts.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Transactions')
    op.drop_table('Accounts')
    op.drop_table('Customers')
    # ### end Alembic commands ###