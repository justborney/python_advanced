"""conflict merge

Revision ID: 11c3e47f7487
Revises: 52dc1fa6c27f, 665ad15a1028
Create Date: 2022-07-02 23:43:21.186311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11c3e47f7487'
down_revision = ('52dc1fa6c27f', '665ad15a1028')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
