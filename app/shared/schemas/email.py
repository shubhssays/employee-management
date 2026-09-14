from typing import TypedDict, Optional

from pydantic import EmailStr
from typing_extensions import Required


class EmailPayload(TypedDict):
    receiver_email: Required[EmailStr]
    subject: Required[str]
    complete_filepath: Optional[str]
    text_body: Optional[str]
    html_body: Optional[str]
