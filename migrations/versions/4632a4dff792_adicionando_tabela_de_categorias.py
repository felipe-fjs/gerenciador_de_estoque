"""adicionando tabela de categorias

Revision ID: 4632a4dff792
Revises: b5f6a42b0b58
Create Date: 2024-09-24 19:59:18.536800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4632a4dff792'
down_revision = 'b5f6a42b0b58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('altered_at', sa.DateTime(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categorias')
    # ### end Alembic commands ###
