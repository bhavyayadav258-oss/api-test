import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Contact Automation API",
    version="1.0.0",
    description="FastAPI contact form backend with Swagger UI.",
)

app.mount("/static", StaticFiles(directory="Static"), name="static")
templates = Jinja2Templates(directory="Templates")

# Configuration from environment variables
MAIL_SENDER_EMAIL = os.environ.get("MAIL_SENDER_EMAIL", "fordemo2511@gmail.com")
MAIL_SENDER_PASSWORD = os.environ.get("MAIL_SENDER_PASSWORD", "tibmaeiotwhjkpfr")
MAIL_RECEIVER_EMAIL = os.environ.get("MAIL_RECEIVER_EMAIL", "bhavya.yadav258@gmail.com")

SUBJECT_OPTIONS = [
    "Internship Inquiry",
    "Project Collaboration",
    "Training Program",
    "General Query",
]


def send_admin_email(name: str, email: str, organization: str, subject: str, message: str) -> None:
    body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Organization: {organization}
Subject: {subject}

Message:
{message}
"""

    msg = MIMEText(body)
    msg["Subject"] = f"New Enquiry - {subject}"
    msg["From"] = MAIL_SENDER_EMAIL
    msg["To"] = MAIL_RECEIVER_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(MAIL_SENDER_EMAIL, MAIL_SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()


def send_user_email(name: str, user_email: str) -> None:
    html = f"""
<h2>Thank You, {name}!</h2>
<p>We have received your enquiry.</p>
<p>Our team will contact you shortly.</p>
<p>Regards,</p>
<h4>Trishul Space Team</h4>
"""

    msg = MIMEText(html, "html")
    msg["Subject"] = "We Received Your Query"
    msg["From"] = MAIL_SENDER_EMAIL
    msg["To"] = user_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(MAIL_SENDER_EMAIL, MAIL_SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Contact Automation API",
        "version": "1.0.0",
    }


@app.get("/", response_class=HTMLResponse)
@app.head("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
def submit(
    name: str = Form(..., example="John Doe"),
    email: EmailStr = Form(..., example="john@example.com"),
    organization: str = Form("", example="Acme Corp"),
    subject: str = Form(..., example="Project Collaboration"),
    message: str = Form(..., example="I am interested in your services."),
):
    if subject not in SUBJECT_OPTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid subject",
                "allowed_subjects": SUBJECT_OPTIONS,
            },
        )

    print("\n" + "=" * 50)
    print(f"NEW SUBMISSION - {datetime.now()}")
    print("=" * 50)
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Organization: {organization}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print("=" * 50 + "\n")

    try:
        send_admin_email(name, email, organization, subject, message)
        send_user_email(name, email)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to send emails", "reason": str(exc)},
        )

    return {
        "success": True,
        "message": "Form submitted successfully",
        "timestamp": datetime.now().isoformat(),
    }
