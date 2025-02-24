"""Now added stages question can be group by stages with many to many relationship.

Revision ID: 92894113d5f3
Revises: ddb23426be39
Create Date: 2025-02-24 10:42:25.418735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92894113d5f3'
down_revision = 'ddb23426be39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_stages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('questions_id', sa.Integer(), nullable=False),
    sa.Column('stage_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['questions_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('questions_stages')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions_stages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('questions_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('stage_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['questions_id'], ['questions.id'], name='questions_stages_questions_id_fkey'),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], name='questions_stages_stage_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='questions_stages_pkey')
    )
    op.drop_table('question_stages')
    # ### end Alembic commands ###
