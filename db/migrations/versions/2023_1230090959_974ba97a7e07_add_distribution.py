"""Add Distribution

Revision ID: 974ba97a7e07
Revises: 
Create Date: 2023-12-30 09:09:59.923182

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '974ba97a7e07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('distribution',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('block', sa.BigInteger(), nullable=False),
    sa.Column('transaction', sa.String(length=66), nullable=False),
    sa.Column('sender', sa.String(length=42), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('input_aix', sa.Numeric(), nullable=False),
    sa.Column('distributed_aix', sa.Numeric(), nullable=False),
    sa.Column('swapped_eth', sa.Numeric(), nullable=False),
    sa.Column('distributed_eth', sa.Numeric(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_distribution_block'), 'distribution', ['block'], unique=False)
    op.create_index(op.f('ix_distribution_sender'), 'distribution', ['sender'], unique=False)
    op.create_index(op.f('ix_distribution_timestamp'), 'distribution', ['timestamp'], unique=False)
    op.create_index(op.f('ix_distribution_transaction'), 'distribution', ['transaction'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_distribution_transaction'), table_name='distribution')
    op.drop_index(op.f('ix_distribution_timestamp'), table_name='distribution')
    op.drop_index(op.f('ix_distribution_sender'), table_name='distribution')
    op.drop_index(op.f('ix_distribution_block'), table_name='distribution')
    op.drop_table('distribution')
    # ### end Alembic commands ###
