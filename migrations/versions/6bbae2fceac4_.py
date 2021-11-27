"""empty message

Revision ID: 6bbae2fceac4
Revises: 
Create Date: 2021-11-22 21:03:24.368856

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6bbae2fceac4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrow',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('borrowed_date', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('returned_date', sa.DateTime(), nullable=True),
    sa.Column('points_used', sa.Integer(), nullable=True),
    sa.Column('book_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('borrower', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['borrower'], ['user_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('borrowing')
    op.alter_column('author', 'first_name',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('author', 'last_name',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'last_name',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('author', 'first_name',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.create_table('borrowing',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('borrowed_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deadline', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('returned_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('points_used', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('book_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('borrower', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], name='borrowing_book_id_fkey'),
    sa.ForeignKeyConstraint(['borrower'], ['user_profile.id'], name='borrowing_borrower_fkey'),
    sa.PrimaryKeyConstraint('id', name='borrowing_pkey')
    )
    op.drop_table('borrow')
    # ### end Alembic commands ###
