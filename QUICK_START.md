# 🚀 Quick Start Guide

## Option 1: Windows (Double-click)
1. Double-click `start.bat`
2. Wait for the server to start
3. Open `index.html` in your browser

## Option 2: Manual Start
1. Install dependencies:
   \`\`\`bash
   pip install flask flask-cors
   \`\`\`

2. Start the server:
   \`\`\`bash
   python app.py
   \`\`\`

3. Open `index.html` in your browser

## ✅ Verification
- Server should show: "Starting Professional Fashion Sizing API..."
- Visit: http://localhost:5000/api/health
- Should return: `{"status": "healthy"}`

## 🔧 Troubleshooting
- **Port 5000 in use**: Change port in `app.py` line: `app.run(port=5001)`
- **Flask not found**: Run `pip install flask flask-cors`
- **CORS errors**: Make sure server is running on localhost:5000

## 📱 Usage
1. Fill in your measurements (chest, shoulders, waist, hips required)
2. Select fit preferences (tailored, classic, relaxed)
3. Choose gender and body type
4. Get professional size recommendations!
