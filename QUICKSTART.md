# 🚀 Quick Start Guide — Kalainayam

## One-Step Setup (Recommended)

### macOS/Linux
```bash
cd /Users/mvnikhitha/Desktop/Kalainayam
chmod +x start.sh
./start.sh
```

### Windows
```cmd
cd C:\Users\mvnikhitha\Desktop\Kalainayam
start.bat
```

This will automatically:
- Set up Python virtual environment
- Install dependencies
- Start backend server on `http://localhost:5000`
- Start frontend server on `http://localhost:8000`

---

## Manual Setup

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
python app.py
```
✅ Backend running on `http://localhost:5000`

### Step 3: Start Frontend Server (new terminal)
```bash
cd frontend
python -m http.server 8000
```
✅ Frontend running on `http://localhost:8000`

### Step 4: Open in Browser
Visit: **http://localhost:8000**

---

## File Structure

```
Kalainayam/
├── frontend/
│   ├── index.html              ← Main homepage
│   ├── css/styles.css          ← All styling
│   ├── js/
│   │   ├── script.js           ← Main app logic
│   │   ├── api.js              ← Backend API client
│   │   ├── renderResults.js    ← Dynamic rendering
│   │   ├── charts.js           ← Visualizations
│   │   └── utils.js            ← Helpers
│   └── pages/                  ← Additional pages
│
├── backend/
│   ├── app.py                  ← Flask API
│   ├── config.py               ← Configuration
│   └── requirements.txt         ← Dependencies
│
└── README.md                    ← Full documentation
```

---

## Key Features

✨ **Dashboard** - Real-time trend analysis (styles, colors, fabrics)
✨ **Collection Generator** - AI suggests designs based on season & audience
✨ **Reports** - Download market insights
✨ **Responsive Design** - Works on desktop & mobile
✨ **Modern UI** - Wine-themed with smooth animations

---

## Pages & Routes

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing page with overview |
| Trends | `/pages/ai-analysis.html` | Detailed trend analysis dashboard |
| Create | `/pages/create-collection.html` | Collection suggestion generator |
| Reports | `/pages/reports.html` | Download & request reports |
| About | `/pages/about.html` | About Kalainayam |

---

## API Endpoints

All endpoints return JSON responses.

```
GET  /api/health                    # Server health check
GET  /api/trends                    # Get trend data
POST /api/suggestions               # Generate suggestions
POST /api/subscribe                 # Newsletter signup
POST /api/request-report            # Request custom report
GET  /api/download-report/<template> # Download PDF
```

### Example API Call
```javascript
// Get trends
fetch('http://localhost:5000/api/trends?region=global&days=28')
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Find process using port 8000
lsof -i :8000

# Kill process (replace PID with actual process ID)
kill -9 <PID>
```

### Python Not Found
Make sure Python 3.8+ is installed:
```bash
python --version
# or
python3 --version
```

### CORS Errors
- Backend must be running on port 5000
- Flask-CORS is already installed in requirements.txt

### Styles Not Loading
- Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)
- Check CSS paths are correct: `../css/styles.css`

### Forms Not Submitting
- Check backend is running
- Open browser DevTools → Network tab to see requests
- Fallback to client-side handling if API unavailable

---

## Development Tips

### Adding a New Feature

1. **Create HTML** in appropriate page
2. **Add JavaScript** in `js/script.js` or new module
3. **Style with CSS** in `css/styles.css`
4. **Add API endpoint** in `backend/app.py`

### Testing API Endpoints

Use `curl` or Postman:
```bash
# Test health
curl http://localhost:5000/api/health

# Test trends
curl http://localhost:5000/api/trends?region=global&days=28

# Test suggestions
curl -X POST http://localhost:5000/api/suggestions \
  -H "Content-Type: application/json" \
  -d '{"season":"spring","audience":"women","price":"mid","focus":"tailoring"}'
```

### Making Changes

1. Edit files in your editor
2. Refresh browser (or use LiveServer for auto-refresh)
3. Backend changes require restart

---

## Next Steps

1. ✅ Website is now working!
2. Connect to real AI models in `ai/models/`
3. Set up database for user data
4. Add user authentication
5. Deploy to production

---

## Support

For issues or questions, check:
- [README.md](README.md) - Full documentation
- API responses in browser console (F12)
- Backend logs in terminal

---

**Happy designing!** 🎨

© 2025 Kalainayam
