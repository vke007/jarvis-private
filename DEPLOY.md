# JARVIS — Complete Deployment Guide
## GitHub + Railway.app — Step by Step

---

## 📁 FOLDER STRUCTURE TO PUSH

```
jarvis-final/
├── backend/
│   ├── server.py          ← Flask API
│   ├── requirements.txt   ← Python packages
│   ├── Procfile           ← How Railway runs the app
│   ├── railway.toml       ← Railway config
│   └── .env.example       ← Environment variables template
└── frontend/
    ├── index.html         ← Complete web app (one file)
    ├── sw.js              ← Service worker (offline)
    ├── manifest.json      ← PWA config
    ├── icon-192.png       ← App icon (generate below)
    └── icon-512.png       ← App icon (generate below)
```

---

## 🎨 STEP 0 — GENERATE YOUR APP ICONS

Open this in a browser and save the canvases:

```html
<!DOCTYPE html>
<html>
<body>
<canvas id="c192" width="192" height="192"></canvas>
<canvas id="c512" width="512" height="512"></canvas>
<script>
function drawIcon(id, size) {
  const c = document.getElementById(id);
  const ctx = c.getContext('2d');
  const g = ctx.createLinearGradient(0,0,size,size);
  g.addColorStop(0,'#00d4ff'); g.addColorStop(1,'#0066aa');
  ctx.fillStyle=g; ctx.fillRect(0,0,size,size);
  ctx.fillStyle='rgba(255,255,255,0.15)';
  ctx.beginPath(); ctx.arc(size/2,size/2,size*.36,0,Math.PI*2); ctx.fill();
  ctx.fillStyle='white';
  ctx.font=`900 ${size*.5}px sans-serif`;
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('J', size/2, size/2);
}
drawIcon('c192',192); drawIcon('c512',512);
</script>
</body>
</html>
```

Right-click each canvas → "Save image as"
→ Save as `icon-192.png` and `icon-512.png` in `frontend/`

---

## 🐙 STEP 1 — CREATE GITHUB REPOSITORY

### 1A. Install Git (if not installed):
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`
- Linux: `sudo apt install git`

### 1B. Create repo on GitHub.com:
1. Go to **github.com** → Sign in
2. Click **"New"** (green button)
3. Name it: `jarvis-private-assistant`
4. Set to **Private** ← IMPORTANT for your private app
5. Click **"Create repository"**

### 1C. Push your code:
```bash
# Navigate to your project folder
cd jarvis-final

# Initialize git
git init

# Create .gitignore (IMPORTANT — never commit secrets)
echo ".env
*.pyc
__pycache__/
*.db
instance/
.DS_Store
node_modules/" > .gitignore

# Add all files
git add .

# First commit
git commit -m "Initial JARVIS deployment"

# Connect to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/jarvis-private-assistant.git

# Push
git branch -M main
git push -u origin main
```

---

## 🚂 STEP 2 — DEPLOY BACKEND ON RAILWAY

### 2A. Create Railway Account:
1. Go to **railway.app**
2. Click **"Login"** → Sign in with GitHub
3. Authorize Railway to access your GitHub

### 2B. Create New Project:
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `jarvis-private-assistant`
4. Railway detects it as Python ✅

### 2C. Configure Root Directory:
1. Click on your service (the box that appeared)
2. Go to **Settings** tab
3. Find **"Root Directory"**
4. Set it to: `backend`
5. Click **Save**

### 2D. Set Environment Variables:
Click **Variables** tab → Add each one:

```
SECRET_KEY          = (generate: python -c "import secrets; print(secrets.token_hex(32))")
OWNER_EMAIL         = your@email.com
OWNER_PASSWORD      = YourStrongPassword123!
OWNER_NAME          = YourName
ANTHROPIC_API_KEY   = sk-ant-your-key-here
```

### 2E. Add PostgreSQL Database:
1. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway auto-sets `DATABASE_URL` ✅
3. No manual config needed

### 2F. Deploy:
1. Click **"Deploy"** button
2. Watch the build logs
3. Once done, click **"View logs"** → should show:
   ```
   ✅  Database ready
   🚀  JARVIS API running on port XXXX
   ```
4. Click **"Generate Domain"** → you get a URL like:
   ```
   https://jarvis-private-assistant.railway.app
   ```

### 2G. Test your API:
```
https://YOUR-URL.railway.app/api/ping
```
Should return: `{"status": "ok", "app": "JARVIS"}`

---

## 🌐 STEP 3 — DEPLOY FRONTEND ON RAILWAY

### Option A: Deploy Frontend on Same Railway Project

1. In Railway, click **"New"** → **"Empty Service"**
2. Add this `package.json` to your `frontend/` folder:

```json
{
  "name": "jarvis-frontend",
  "scripts": {
    "start": "npx serve . -p $PORT"
  },
  "dependencies": {
    "serve": "^14.2.0"
  }
}
```

3. Go to the new service → Settings → Root Directory → `frontend`
4. Deploy → Get URL like `jarvis-frontend.railway.app`

### Option B: Deploy Frontend on Vercel (FREE, recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend folder
cd jarvis-final/frontend

# Deploy
vercel

# Follow prompts → Get URL:
# https://jarvis-frontend.vercel.app
```

### Option C: Deploy Frontend on Netlify (FREE)
1. Go to **netlify.com**
2. Drag and drop your `frontend/` folder
3. Get URL instantly ✅

---

## 🔗 STEP 4 — CONNECT FRONTEND TO BACKEND

### Update the API URL in your frontend:

1. Open `frontend/index.html`
2. Find this line:
```javascript
let API = localStorage.getItem('jarvis_api') || 'http://localhost:5000/api';
```
3. Change it to your Railway URL:
```javascript
let API = localStorage.getItem('jarvis_api') || 'https://YOUR-APP.railway.app/api';
```

### Or update it from inside the app:
1. Login to JARVIS
2. Go to **⚙ Settings**
3. Update "Backend Server URL" to your Railway URL
4. Click **SAVE**

---

## 📱 STEP 5 — INSTALL AS MOBILE APP

### iPhone/iPad:
1. Open your frontend URL in **Safari**
2. Tap Share button (⎙)
3. Tap **"Add to Home Screen"**
4. Tap **"Add"**
5. JARVIS icon on your home screen ✅

### Android:
1. Open URL in **Chrome**
2. Tap menu (⋮) → **"Add to Home Screen"**
3. Or look for the install banner at the bottom
4. Tap **"Install"** ✅

---

## 🔒 STEP 6 — SECURE YOUR DEPLOYMENT

### Only YOU can log in:
- Your `OWNER_EMAIL` and `OWNER_PASSWORD` are set in Railway env vars
- No registration page exists
- Anyone else gets "ACCESS DENIED"

### Change your password:
1. Go to Railway → Your service → Variables
2. Update `OWNER_PASSWORD`
3. Redeploy (automatic)

### Regenerate SECRET_KEY periodically:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Update in Railway Variables.

---

## 🔄 STEP 7 — UPDATING YOUR APP

### Push updates:
```bash
# Make your changes

# Stage and commit
git add .
git commit -m "Update: improved UI and new features"

# Push to GitHub
git push origin main
```

Railway automatically redeploys when you push to GitHub ✅

### Update UI/Logo without coding:
1. Open JARVIS → **◧ UI / LOGO** module
2. Use the color pickers → **APPLY THEME**
3. Type new name → **UPDATE**
4. Upload logo image
5. Changes save instantly in your browser
6. To make permanent: edit `index.html` CSS variables

---

## 🛡️ STEP 8 — SAFETY CONTROLS

### To disable any feature instantly:
1. Login to JARVIS
2. Go to **⚡ SAFETY CTRL**
3. Toggle OFF any feature:
   - Web Search
   - AI Responses
   - Code Generation
   - Voice
   - Health Tracking

### Emergency kill all AI:
Click **"⚡ KILL ALL AI FEATURES"** — instant off switch

### Via voice:
Say "Hey Jarvis, kill all" to emergency disable

---

## 📊 MONITORING YOUR APP

### Railway Dashboard:
- View real-time logs
- Monitor memory usage
- Check deployment status
- View database usage

### Check API health:
```
https://YOUR-APP.railway.app/api/ping
```

---

## 💰 RAILWAY PRICING

### Free Tier:
- $5 free credit per month
- More than enough for personal use
- PostgreSQL included free

### If you exceed free tier:
- ~$5-10/month for hobby project
- No surprise charges

---

## 🔧 TROUBLESHOOTING

### "Cannot connect to server":
1. Check your Railway deployment is running
2. Go to Settings → update API URL to Railway URL
3. Make sure URL ends with `/api` (no trailing slash on base)

### "ACCESS DENIED" on login:
1. Check OWNER_EMAIL matches exactly (case-sensitive)
2. Check OWNER_PASSWORD in Railway variables
3. No spaces before/after values

### Build failing on Railway:
1. Check build logs in Railway dashboard
2. Common fix: ensure `requirements.txt` is correct
3. Root directory must be set to `backend`

### Database errors:
1. Check PostgreSQL service is running in Railway
2. The `DATABASE_URL` should be auto-set by Railway
3. Try redeploying the backend service

### PWA not installing:
1. Must be served over HTTPS (Railway/Vercel provide this)
2. manifest.json must be accessible
3. Try Chrome or Safari (best support)

---

## ✅ FINAL CHECKLIST

- [ ] Icons generated (icon-192.png, icon-512.png)
- [ ] GitHub repo created (private)
- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Backend deployed on Railway
- [ ] Environment variables set
- [ ] PostgreSQL added
- [ ] Backend URL tested (/api/ping)
- [ ] Frontend deployed (Vercel/Netlify/Railway)
- [ ] Frontend connected to backend URL
- [ ] Login tested with your email/password
- [ ] App installed on mobile
- [ ] Voice "Hey Jarvis" tested
- [ ] Safety controls verified

---

## 📞 QUICK REFERENCE

```
Login URL:     https://your-frontend.vercel.app
API URL:       https://your-app.railway.app/api
API Health:    https://your-app.railway.app/api/ping
GitHub Repo:   https://github.com/YOU/jarvis-private-assistant
Railway:       https://railway.app/dashboard
Vercel:        https://vercel.com/dashboard
```

---

**Your JARVIS is now fully deployed, private, and accessible from anywhere!** 🚀
