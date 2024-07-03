# 사용하기 전 네이버 메일 환경설정에서 pop3/smtp 사용으로 설정 바꿔야 함

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app = FastAPI()

class EmailRequest(BaseModel):
    from_email: str
    to_email: str
    subject: str
    body: str
    verification_url: str

@app.post("/send_email")
def send_email(email_request: EmailRequest):
    smtp_server = "smtp.naver.com" #smtp server 설정 (추후 google로 변경 예정)
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login("example@naver.com", "example") # naver id, pw

        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_request.subject
        msg['From'] = email_request.from_email
        msg['To'] = email_request.to_email

        # 버튼 구현하기 위한 코드
        html = f""" 
        <html>
          <body>
            <p>{email_request.body}</p>
            <a href="{email_request.verification_url}" style="background-color:#4CAF50;border:none;color:white;padding:15px 32px;text-align:center;text-decoration:none;display:inline-block;font-size:16px;margin:4px 2px;cursor:pointer;">Verify Account</a>
          </body>
        </html>
        """

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        server.send_message(msg)
        server.quit()
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
