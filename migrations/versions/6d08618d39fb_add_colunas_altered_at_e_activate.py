"""add colunas altered_at e activate

Revision ID: 6d08618d39fb
Revises: 729a3a12a963
Create Date: 2024-09-16 20:07:29.597024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d08618d39fb'
down_revision = '729a3a12a963'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('altered_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('activate', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('activate')
        batch_op.drop_column('altered_at')

    # ### end Alembic commands ###
