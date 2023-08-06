"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/23 2:06 下午
@Software: PyCharm
@File    : v1.2.0.a.py
@E-mail  : victor.xsyang@gmail.com
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "v1.2.0.a"
down_revision = "v0.9.0.a"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("trials") as batch_op:
        batch_op.alter_column(
            "state",
            type_=sa.Enum("RUNNING", "COMPLETE", "STOP", "FAIL", "WAITING", name="trialstate"),
            existing_type=sa.Enum("RUNNING", "COMPLETE", "STOP", "FAIL", name="trialstate"),
        )


def downgrade():
    with op.batch_alter_table("trials") as batch_op:
        batch_op.alter_column(
            "state",
            type_=sa.Enum("RUNNING", "COMPLETE", "STOP", "FAIL", name="trialstate"),
            existing_type=sa.Enum(
                "RUNNING", "COMPLETE", "STOP", "FAIL", "WAITING", name="trialstate"
            ),
        )
