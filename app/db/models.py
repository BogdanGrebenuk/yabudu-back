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
    sa.Column('token', sa.Text, nullable=True),
    sa.Column('interests', sa.JSON(), nullable=False)
)

Participation = sa.Table(
    'participation',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('user_id', sa.Text, sa.ForeignKey('user.id'), nullable=False),
    sa.Column('event_id', sa.Text, sa.ForeignKey('event.id'), nullable=False),
    sa.Column('type', sa.Boolean(), nullable=False),
    sa.Column('role', sa.Boolean(), nullable=False)
)

Event = sa.Table(
    'event',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('description', sa.Text, nullable=True),
    sa.Column('start_at', sa.DateTime(), nullable=False),
    sa.Column('end_at', sa.DateTime(), nullable=True),
    sa.Column('x', sa.Float(), nullable=True),
    sa.Column('y', sa.Float(), nullable=True),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('interests', sa.JSON(), nullable=False),
    sa.Column('image', sa.Text(), nullable=True)
)

Message = sa.Table(
    'message',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('event_id', sa.Text, sa.ForeignKey('event.id'), nullable=False),
    sa.Column('user_id', sa.Text, sa.ForeignKey('user.id'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text, nullable=False),
)

Feedback = sa.Table(
    'feedback',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('event_id', sa.Text, sa.ForeignKey('event.id'), nullable=False),
    sa.Column('user_id', sa.Text, sa.ForeignKey('user.id'), nullable=False),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('text', sa.Text, nullable=True),
)
