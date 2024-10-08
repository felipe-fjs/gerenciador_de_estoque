"""adicionando coluna categorias à Product

Revision ID: 67ab76199422
Revises: 4632a4dff792
Create Date: 2024-09-24 20:10:52.506808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67ab76199422'
down_revision = '4632a4dff792'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categorias', ['categoria'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('categoria')

    # ### end Alembic commands ###
