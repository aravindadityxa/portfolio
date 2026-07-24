# Portfolio Contact Form Backend

A production-ready FastAPI backend for portfolio contact form submissions with email notifications, database storage, and rate limiting.

## Features

- **FastAPI** - Fast, modern Python web framework
- **Email Notifications** - Send contact form submissions to your Gmail
- **Database Storage** - SQLite by default, supports MySQL and PostgreSQL
- **Rate Limiting** - Prevent spam with IP-based rate limiting (5 requests per hour)
- **Input Validation** - Pydantic models with strict validation and sanitization
- **CORS Support** - Secure cross-origin requests from frontend
- **Logging** - Comprehensive logging for debugging and monitoring
- **Error Handling** - Proper HTTP status codes and error messages
- **Production Ready** - Environment variables, security best practices, and deployment guides

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (default), MySQL, PostgreSQL
- **Email**: SMTP (Gmail, Outlook, custom servers)
- **Validation**: Pydantic
- **Server**: Uvicorn

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── config.py            # Configuration from environment variables
├── schemas.py           # Pydantic request/response models
├── models.py            # SQLAlchemy database models
├── email_service.py     # Email sending functionality
├── rate_limiter.py      # Rate limiting logic
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Local Setup

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Gmail account with App Password (for SMTP)

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Create Environment File

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Generate from Gmail settings
SMTP_FROM_EMAIL=your-email@gmail.com
OWNER_EMAIL=your-email@gmail.com
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 4. Gmail Setup for SMTP

To use Gmail as your email provider:

1. Enable 2-Factor Authentication: https://support.google.com/accounts/answer/185833
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password
   - Use this in `SMTP_PASSWORD` in `.env`

### 5. Run Backend Locally

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Test API

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Submit Contact Form:**
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, I am interested in your services!"
  }'
```

## API Endpoints

### POST /api/contact
Submit a contact form message.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Your message here (minimum 10 characters)"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Thank you for your message! I'll get back to you soon.",
  "submission_id": 1
}
```

**Response (Error - 429 Rate Limited):**
```json
{
  "detail": "Too many requests. Please try again later."
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### GET /api/submissions
Get recent contact form submissions (admin use).

**Response:**
```json
{
  "total": 42,
  "submissions": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "message": "Your message...",
      "status": "email_sent",
      "submitted_at": "2024-01-15T10:30:45.123456",
      "ip_address": "192.168.1.1"
    }
  ]
}
```

## Deployment

### Option 1: Deploy on Render

**Render** (recommended for simplicity):

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub or email
   - Create new project

2. **Connect GitHub Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Build Settings**
   - **Name**: `portfolio-contact-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`

4. **Add Environment Variables**
   - Click "Environment"
   - Add all variables from `.env.example`:
     - `ENVIRONMENT=production`
     - `DEBUG=False`
     - `DATABASE_URL=sqlite:///./contact_messages.db`
     - `SMTP_SERVER=smtp.gmail.com`
     - `SMTP_PORT=587`
     - `SMTP_USER=your-email@gmail.com`
     - `SMTP_PASSWORD=your-app-password`
     - `SMTP_FROM_EMAIL=your-email@gmail.com`
     - `OWNER_EMAIL=your-email@gmail.com`
     - `ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be at: `https://portfolio-contact-api.onrender.com`

6. **Update Frontend URL**
   - In `script.js`, update the API URL:
   ```javascript
   window.CONTACT_API_URL = 'https://portfolio-contact-api.onrender.com/api/contact';
   ```

### Option 2: Deploy on Railway

**Railway** (good for quick deploys):

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub
   - Create new project

2. **Connect to GitHub**
   - Select "Deploy from GitHub repo"
   - Authorize and select your repository

3. **Configure Service**
   - Railway will auto-detect Python
   - Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Click "Add Variable"
   - Add all from `.env.example`

5. **Deploy**
   - Click "Deploy"
   - Get your URL from the Railway dashboard

### Option 3: Deploy on Heroku (Legacy)

Heroku's free tier is no longer available, but you can still use it with a paid account.

### Reverse Proxy Setup (Using Nginx)

If deploying on a VPS with your own domain:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Database

### SQLite (Default)

Default SQLite database is auto-created at `contact_messages.db`

### MySQL

To use MySQL:

1. **Install MySQL client**:
   ```bash
   pip install pymysql
   ```

2. **Update `.env`**:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost/portfolio_db
   ```

3. **Create database**:
   ```bash
   mysql -u user -p
   CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### PostgreSQL

To use PostgreSQL:

1. **Install psycopg2**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update `.env`**:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/portfolio_db
   ```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file. Use `.env.example` for reference.
2. **Input Validation**: All inputs are validated and sanitized.
3. **Rate Limiting**: Limited to 5 requests per hour per IP.
4. **HTTPS**: Always use HTTPS in production.
5. **CORS**: Configure `ALLOWED_ORIGINS` to only your domains.
6. **Logging**: Sensitive data is not logged.
7. **Email Credentials**: Use App Passwords, never store main password.

## Troubleshooting

### "SMTP authentication failed"
- Check SMTP credentials in `.env`
- Verify Gmail App Password (not regular password)
- Ensure 2FA is enabled on Gmail account

### "Database is locked" (SQLite)
- SQLite is single-writer, avoid concurrent writes
- For production, use MySQL or PostgreSQL

### "CORS error in browser"
- Ensure frontend URL is in `ALLOWED_ORIGINS`
- Check API URL in frontend matches backend deployment URL

### "Rate limit exceeded"
- Wait 1 hour or manually reset in rate limiter
- Configure `RATE_LIMIT_MAX_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS` in `.env`

### "Form not submitting"
- Check browser console for errors
- Verify API URL is correct
- Ensure backend is running and accessible
- Check CORS headers in network tab

## Performance Tips

1. Use PostgreSQL for production (better than SQLite)
2. Enable caching for health checks
3. Add CDN for static assets
4. Monitor logs regularly
5. Set up automated backups for database

## License

MIT

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for errors
3. Check FastAPI documentation: https://fastapi.tiangolo.com
4. Test API endpoints with curl or Postman

## Future Enhancements

- [ ] Email templates with MJML
- [ ] Admin dashboard for submissions
- [ ] Two-factor authentication for admin
- [ ] Webhook notifications (Slack, Discord)
- [ ] Export submissions to CSV
- [ ] Scheduled email digests
- [ ] File upload support
