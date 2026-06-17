"""add check constraint to todo state

Revision ID: ea64c1d872d4
Revises: c9395b812b92
Create Date: 2026-06-10 19:35:08.962552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea64c1d872d4'
down_revision: Union[str, Sequence[str], None] = 'c9395b812b92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cria a restrição de forma segura para o SQLite
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_todos_state',
            "state IN ('draft', 'todo', 'doing', 'done', 'trash')"
        )

def downgrade() -> None:
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_constraint('ck_todos_state', type_='check')
