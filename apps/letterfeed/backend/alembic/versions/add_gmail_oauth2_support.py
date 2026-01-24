"""Add Gmail OAuth2 credentials table.

Revision ID: add_gmail_oauth2
Revises: ce35472309a4
Create Date: 2026-01-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_gmail_oauth2"
down_revision = "ce35472309a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create gmail_oauth2_credentials table."""
    op.create_table(
        "gmail_oauth2_credentials",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("encrypted_access_token", sa.Text(), nullable=False),
        sa.Column("encrypted_refresh_token", sa.Text(), nullable=False),
        sa.Column("token_expiry", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_gmail_oauth2_credentials_email", "gmail_oauth2_credentials", ["email"]
    )


def downgrade() -> None:
    """Drop gmail_oauth2_credentials table."""
    op.drop_index(
        "ix_gmail_oauth2_credentials_email", table_name="gmail_oauth2_credentials"
    )
    op.drop_table("gmail_oauth2_credentials")
