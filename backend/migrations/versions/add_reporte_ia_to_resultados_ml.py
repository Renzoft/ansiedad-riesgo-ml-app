"""add_reporte_ia_to_resultados_ml

Revision ID: add_reporte_ia
Revises: dd12ce3ce73f
Create Date: 2024-06-19 19:39:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_reporte_ia'
down_revision = 'dd12ce3ce73f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('resultados_ml', sa.Column('reporte_ia', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('resultados_ml', 'reporte_ia')