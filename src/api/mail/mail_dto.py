from pydantic import BaseModel

class EmailRequest(BaseModel):
    from_email: str
    to_email: str
    subject: str
    body: str
    verification_url: str
