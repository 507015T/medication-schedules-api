"""Initial migrate

Revision ID: 1b143abe90e5
Revises:
Create Date: 2025-04-29 10:34:26.638286

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b143abe90e5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('medication_name', sa.String(length=255), nullable=False),
        sa.Column('frequency', sa.SmallInteger(), nullable=False),
        sa.Column('duration_days', sa.SmallInteger(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.CheckConstraint('duration_days > 0', name='check_correctness_duration_days'),
        sa.CheckConstraint(
            'frequency >= 1 AND frequency <= 15', name='check_correctness_frequency'
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_schedules_frequency'), 'schedules', ['frequency'], unique=False
    )
    op.create_index(op.f('ix_schedules_id'), 'schedules', ['id'], unique=False)
    op.create_index(
        op.f('ix_schedules_medication_name'),
        'schedules',
        ['medication_name'],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedules_medication_name'), table_name='schedules')
    op.drop_index(op.f('ix_schedules_id'), table_name='schedules')
    op.drop_index(op.f('ix_schedules_frequency'), table_name='schedules')
    op.drop_table('schedules')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
