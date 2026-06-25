# Contact Automation API

A Flask-based contact form API that processes form submissions and sends automated emails to both admins and users.

## Features

✅ Contact form submission endpoint  
✅ Automated email notifications (admin + user)  
✅ Health check endpoint  
✅ Environment variable configuration  
✅ Input validation  
✅ Error handling  

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
MAIL_SENDER_EMAIL=your-sender@gmail.com
MAIL_SENDER_PASSWORD=your-app-password
MAIL_RECEIVER_EMAIL=admin@company.com
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Run the Server

```bash
python3 app.py
```

Server starts at: `http://localhost:5000`

---

## API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-25T10:30:00.123456",
  "service": "Contact Automation API",
  "version": "1.0.0"
}
```

**Test:**
```bash
curl http://localhost:5000/health
```

---

### 2. Home Page
**GET** `/`

Returns the contact form HTML page.

**Test:**
```bash
curl http://localhost:5000/
```

---

### 3. Submit Contact Form
**POST** `/submit`

Submit contact form and send emails.

**Content-Type:** `application/x-www-form-urlencoded`

**Required Fields:**
- `name` (string) - Full name
- `email` (string) - Valid email address
- `subject` (string) - One of: "Internship Inquiry", "Project Collaboration", "Training Program", "General Query"
- `message` (string) - Message content

**Optional Fields:**
- `organization` (string) - Organization/Company name

**Success Response (200):**
```json
{
  "success": true,
  "message": "Form submitted successfully",
  "timestamp": "2026-06-25T10:30:00.123456"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid email address"
}
```

---

## Testing Examples

### cURL

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Submit Form:**
```bash
curl -X POST http://localhost:5000/submit \
  -d "name=John Doe" \
  -d "email=john@example.com" \
  -d "organization=Acme Corp" \
  -d "subject=Internship Inquiry" \
  -d "message=I am interested in your internship program"
```

### Python

```python
import requests

data = {
    'name': 'Jane Smith',
    'email': 'jane@example.com',
    'organization': 'Tech Corp',
    'subject': 'Project Collaboration',
    'message': 'Lets discuss collaboration opportunities'
}

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Submit form
response = requests.post('http://localhost:5000/submit', data=data)
print(response.json())
```

### JavaScript/Fetch

```javascript
// Health check
fetch('http://localhost:5000/health')
  .then(res => res.json())
  .then(data => console.log(data));

// Submit form
const formData = new FormData();
formData.append('name', 'John Doe');
formData.append('email', 'john@example.com');
formData.append('organization', 'Company Inc');
formData.append('subject', 'General Query');
formData.append('message', 'Your message here');

fetch('http://localhost:5000/submit', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Email Configuration

### Gmail Setup (Recommended)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Windows Computer" (or your device)
   - Copy the generated 16-character password
3. Update `.env`:
   ```
   MAIL_SENDER_EMAIL=your-email@gmail.com
   MAIL_SENDER_PASSWORD=your-app-password
   ```

---

## Project Structure

```
Contact_Automation/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (DO NOT commit)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── Static/
│   └── style.css         # CSS styles
├── Templates/
│   └── index.html        # Contact form HTML
└── README.md             # This file
```

---

## Error Handling

| Status | Error | Solution |
|--------|-------|----------|
| 400 | "Name is required" | Provide `name` field |
| 400 | "Invalid email address" | Use valid email format |
| 400 | "Subject is required" | Select a subject |
| 400 | "Message is required" | Provide message content |
| 500 | "Failed to process submission" | Check email configuration in `.env` |

---

## Logs

Submissions are logged to the console with timestamps:
```
==================================================
NEW SUBMISSION - 2026-06-25 10:30:00.123456
==================================================
Name: John Doe
Email: john@example.com
Organization: Acme Corp
Subject: Internship Inquiry
Message: I am interested...
==================================================
```

---

## License

MIT
