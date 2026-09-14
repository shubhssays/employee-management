from pydantic import EmailStr, BaseModel, Field


class EmailPayload(BaseModel):
    receiver_email: list[EmailStr] | EmailStr = Field(description="List of receivers")
    subject: str = Field(description="Subject of email")
    complete_filepath: str | None = Field(default=None, description="Complete filepath of attachment")
    text_body: str | None = Field(default=None, description="Text of email")
    html_body: str | None = Field(default=None, description="HTML of email")
