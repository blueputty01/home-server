from datetime import datetime

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for the access token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data encoded in the JWT."""

    username: str | None = None


class GmailOAuth2Credential(BaseModel):
    """Schema for Gmail OAuth2 credentials (public view, no tokens)."""

    email: str
    token_expiry: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class GmailOAuth2AuthRequest(BaseModel):
    """Request to initiate Gmail OAuth2 authorization."""

    redirect_uri: str = Field(
        ..., description="Where to redirect after user approves"
    )


class GmailOAuth2CallbackRequest(BaseModel):
    """Callback request after user authorizes."""

    code: str = Field(..., description="Authorization code from Google")
    state: str | None = Field(default=None, description="State parameter for security")
