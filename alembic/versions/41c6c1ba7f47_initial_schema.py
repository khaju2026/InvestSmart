from alembic import op
import sqlalchemy as sa

# Identificadores da migration
revision = 'xxxx_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True, index=True),
        sa.Column('senha_hash', sa.String, nullable=False),
        sa.Column('cpf', sa.String, nullable=False, unique=True, index=True),
    )

    op.create_table(
        'investimentos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('valor', sa.Float, nullable=False),
        sa.Column('usuario_id', sa.Integer, sa.ForeignKey('usuarios.id')),
    )

    op.create_table(
        'transacoes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tipo', sa.String, nullable=False),
        sa.Column('quantidade', sa.Float, nullable=False),
        sa.Column('preco', sa.Float, nullable=False),
        sa.Column('data', sa.String, nullable=False),
        sa.Column('investimento_id', sa.Integer, sa.ForeignKey('investimentos.id')),
        sa.Column('usuario_id', sa.Integer, sa.ForeignKey('usuarios.id')),
    )

def downgrade() -> None:
    op.drop_table('transacoes')
    op.drop_table('investimentos')
    op.drop_table('usuarios')
