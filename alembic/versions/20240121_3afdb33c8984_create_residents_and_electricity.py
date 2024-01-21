"""create residents and electricity

Revision ID: 3afdb33c8984
Revises: 
Create Date: 2024-01-21 19:18:59.092316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3afdb33c8984'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('residents',
    sa.Column('home_number', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_residents_id'), 'residents', ['id'], unique=False)
    op.create_table('electricity_readings',
    sa.Column('resident_id', sa.Integer(), nullable=False),
    sa.Column('current_reading', sa.Integer(), nullable=False),
    sa.Column('payment_status', sa.Boolean(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.ForeignKeyConstraint(['resident_id'], ['residents.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_electricity_readings_id'), 'electricity_readings', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_electricity_readings_id'), table_name='electricity_readings')
    op.drop_table('electricity_readings')
    op.drop_index(op.f('ix_residents_id'), table_name='residents')
    op.drop_table('residents')
    # ### end Alembic commands ###
