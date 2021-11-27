import sqlalchemy as sa


metadata = sa.MetaData()


User = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('username', sa.Text, nullable=False),
    sa.Column('inst_username', sa.Text, nullable=False),
    sa.Column('email', sa.Text, nullable=False, unique=True),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('token', sa.Text, nullable=True)
)
