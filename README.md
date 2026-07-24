# Aravind Adityaa - Portfolio Website

A professional portfolio website featuring a full-stack contact form with email notifications, built with HTML/CSS/JavaScript frontend and FastAPI backend.

## 🌟 Features

- **Responsive Portfolio Website** - Mobile-first design, works on all devices
- **Contact Form** - Client-side validation with backend API integration
- **Email Notifications** - Automatic email sent via Gmail SMTP
- **Database Storage** - Contact submissions stored in SQLite
- **Rate Limiting** - Prevents spam (5 requests per hour per IP)
- **Input Validation** - Sanitized against XSS attacks
- **CORS Protection** - Secure cross-origin requests
- **Production Ready** - Fully configured for deployment

## 🛠 Technologies

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Responsive design with flexbox/grid
- Smooth animations and transitions
- Font Awesome icons, Google Fonts

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy ORM with SQLite database
- Pydantic data validation
- SMTP for email notifications
- Uvicorn ASGI server

**Deployment:**
- Frontend: GitHub Pages, Vercel, or Netlify
- Backend: Render, Railway, or self-hosted

## 📦 Installation

### Prerequisites
- Python 3.8+
- Gmail account (for SMTP)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   ```

2. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your Gmail App Password
   ```

4. **Run backend**
   ```bash
   python -m uvicorn main:app --reload
   ```

5. **Open frontend**
   - Open `index.html` in browser
   - Or use: `python -m http.server 8080` (from root directory)

## 🚀 Deployment

### Backend Deployment (Render)

1. Push code to GitHub
2. Create Render account at https://render.com
3. New Web Service → Select GitHub repo
4. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variables from `.env.example`
6. Deploy

### Frontend Deployment (GitHub Pages)

1. Repository → Settings → Pages
2. Select `main` branch as source
3. Site available at: `https://username.github.io/portfolio`

### Connect Frontend to Backend

Update `window.CONTACT_API_URL` in `script.js`:
```javascript
window.CONTACT_API_URL = 'https://your-backend-url.onrender.com/api/contact';
```

## 📋 Environment Variables

Create `.env` file in `backend/` directory:

```env
ENVIRONMENT=production
DEBUG=False

# Database
DATABASE_URL=sqlite:///./contact_messages.db

# Gmail SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=True

OWNER_EMAIL=your-email@gmail.com

# Frontend URLs
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
SECRET_KEY=generate-a-strong-random-key
```

**Getting Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Generate password (16 characters)
4. Copy to `.env`

## 📁 Project Structure

```
portfolio/
├── index.html              # Main portfolio page
├── style.css              # Styling
├── script.js              # Frontend logic
├── README.md              # This file
│
├── assets/
│   ├── documents/
│   │   └── Resume.pdf
│   └── images/
│       ├── profile/
│       └── certificates/
│
└── backend/
    ├── main.py           # FastAPI app
    ├── config.py         # Configuration
    ├── models.py         # Database models
    ├── schemas.py        # Pydantic validation
    ├── email_service.py  # Email sending
    ├── rate_limiter.py   # Rate limiting
    ├── requirements.txt  # Dependencies
    ├── .env.example      # Template (commit to git)
    ├── .gitignore
    └── contact_messages.db  # Database (auto-created)
```

## 🔒 Security

- ✅ Input validation and sanitization
- ✅ Rate limiting by IP address
- ✅ CORS protection
- ✅ Environment variables for secrets
- ✅ No hardcoded credentials
- ✅ `.env` excluded from git
- ✅ HTTPS ready for production

## 📊 API Endpoints

### POST /api/contact
Submit contact form message
```json
Request: {
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Your message..."
}

Response: {
  "success": true,
  "message": "Thank you for your message!",
  "submission_id": 1
}
```

### GET /api/health
Health check endpoint

### GET /api/submissions
Retrieve all contact submissions (admin)

### GET /docs
Interactive API documentation (Swagger UI)

## 🧪 Testing

1. **Start backend**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Test API** → Visit http://localhost:8000/docs

3. **Test contact form** → Open `index.html` and submit

4. **Check email** → Gmail inbox should receive notification

## 📝 Troubleshooting

### Email not sending
- Verify Gmail 2-Factor Authentication is enabled
- Check `SMTP_PASSWORD` is 16-character App Password (not Gmail password)
- Verify `SMTP_USER` is your Gmail email
- Check `.env` file is in `backend/` directory

### Form not submitting
- Check browser console for errors (F12)
- Verify backend is running
- Check `window.CONTACT_API_URL` in `script.js`

### Backend won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check `.env` file exists in `backend/` directory
- Review error messages for missing dependencies

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Aravind Adityaa**
- GitHub: [@aravindadityxa](https://github.com/aravindadityxa)
- LinkedIn: [aravindadityaa](https://linkedin.com/in/aravindadityaa)
- Email: aravindadityaa912006@gmail.com

## 🙏 Acknowledgments

Built with FastAPI, SQLAlchemy, and vanilla JavaScript.
Styled with modern CSS3 and responsive design principles.
