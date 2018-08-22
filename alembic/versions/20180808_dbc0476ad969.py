"""init

Revision ID: dbc0476ad969
Revises: 
Create Date: 2018-08-08 19:33:26.691423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbc0476ad969'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Graph_experiment',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('a', sa.Integer(), nullable=False),
    sa.Column('b', sa.Integer(), nullable=False),
    sa.Column('c', sa.Integer(), nullable=False),
    sa.Column('d', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Graph_experiment'))
    )
    op.create_table('Spectra',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=32), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Spectra')),
    sa.UniqueConstraint('label', name=op.f('uq_Spectra_label'))
    )
    op.create_table('Spectra_detail',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Spectra_detail')),
    sa.UniqueConstraint('index', name=op.f('uq_Spectra_detail_index'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('name', name=op.f('uq_users_name'))
    )
    op.create_table('FTIRModel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('magic', sa.Text(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_FTIRModel_creator_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_FTIRModel')),
    sa.UniqueConstraint('name', name=op.f('uq_FTIRModel_name'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('FTIRModel')
    op.drop_table('users')
    op.drop_table('Spectra_detail')
    op.drop_table('Spectra')
    op.drop_table('Graph_experiment')
    # ### end Alembic commands ###