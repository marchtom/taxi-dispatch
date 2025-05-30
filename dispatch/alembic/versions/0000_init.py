"""init

Revision ID: 0000
Revises: 
Create Date: 2025-05-19 20:59:47.023215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('taxi',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('callback_url', sa.String(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('x_start', sa.Integer(), nullable=False),
    sa.Column('y_start', sa.Integer(), nullable=False),
    sa.Column('x_stop', sa.Integer(), nullable=False),
    sa.Column('y_stop', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trip')
    op.drop_table('taxi')
    # ### end Alembic commands ###
