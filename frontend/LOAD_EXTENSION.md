# How to Load Sidebar Scholar Extension in Chrome

## Step-by-Step Instructions

### 1. Open Chrome Extensions Page
- Open Chrome browser
- Navigate to `chrome://extensions/` in the address bar
- OR go to: Menu (⋮) → Extensions → Manage Extensions

### 2. Enable Developer Mode
- Toggle **"Developer mode"** switch ON (located in top-right corner)

### 3. Load the Extension
- Click **"Load unpacked"** button
- Navigate to and select the folder: `/Users/jay/projects/Sidebar-Scholar/frontend`
- Click **"Select"** or **"Open"**

### 4. Verify Installation
- You should see "Sidebar Scholar" appear in your extensions list
- The extension icon should appear in your Chrome toolbar (puzzle piece icon if no custom icon)

### 5. Configure Settings
- Click the extension icon in the toolbar
- Click the ⚙️ settings button
- Set **Backend Server URL** to: `http://localhost:3000` (or your backend URL)
- Optionally set API Provider and API Key override
- Click **"Save Settings"**

### 6. Start Your Backend Server
Before using the extension, make sure your backend is running:
```bash
cd backend
python main.py
# OR
uvicorn main:app --reload --port 3000
```

**Note:** The backend folder is separate from the frontend. Make sure you're in the project root when navigating to `backend/`.

### 7. Test the Extension
- Navigate to any webpage
- Click the Sidebar Scholar extension icon
- The sidebar should open on the right
- Type a question about the page and hit Send

## Troubleshooting

### Extension won't load
- Make sure you're selecting the folder containing `manifest.json`
- Check that all required files exist: `background.js`, `content.js`, `sidebar.html`, `sidebar.js`, `sidebar.css`
- Check Chrome's error console: Click "Errors" button on the extension card

### Sidebar doesn't open
- Check browser console for errors (Right-click extension icon → Inspect popup)
- Verify `manifest.json` has correct `side_panel` configuration

### Can't connect to backend
- Make sure backend server is running on `http://localhost:3000`
- Check backend URL in extension settings
- Verify CORS is enabled in backend (should be `*` for development)

### Missing icons warning
- Chrome will use default icons if icon files are missing
- To add custom icons, create an `icons/` folder with:
  - `icon16.png` (16x16 pixels)
  - `icon48.png` (48x48 pixels)
  - `icon128.png` (128x128 pixels)

## Quick Reload After Changes
- After making code changes, click the **refresh icon** (↻) on the extension card
- Or disable and re-enable the extension

## Uninstall
- Click "Remove" on the extension card
- Or toggle the extension off to disable it temporarily
