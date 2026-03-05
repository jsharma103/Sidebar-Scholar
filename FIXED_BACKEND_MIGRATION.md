# Fixed Backend Migration Guide

This document explains the changes made to use a fixed backend URL instead of user-configurable backend.

## Why This Change?

### Benefits
✅ **Better Security** - Users can't point to malicious servers  
✅ **Simpler UX** - No configuration needed, works out of the box  
✅ **Faster Chrome Store Review** - Narrow permissions are easier to justify  
✅ **Better Support** - One backend to maintain and monitor  
✅ **Cost Control** - You can implement rate limiting, caching, etc.

### Trade-offs
❌ Users can't self-host their own backend  
❌ Less flexibility for enterprise deployments

**For a public Chrome Web Store extension, fixed backend is the recommended approach.**

---

## What Changed

### 1. Backend URL is Now Fixed
- **Before:** Users could configure backend URL in settings
- **After:** Backend URL is hardcoded in `background.js` as `BACKEND_URL` constant

### 2. Settings Simplified
- **Removed:** Backend URL input field
- **Kept:** API Provider and API Key override (still useful for power users)

### 3. Host Permissions Narrowed
- **Before:** `"https://*/*"` and `"http://*/*"` (all websites)
- **After:** `"https://your-backend.railway.app/*"` (only your backend)

---

## Files Modified

1. **`frontend/background.js`**
   - Added `BACKEND_URL` constant at top
   - Removed `backendUrl` from settings retrieval
   - Uses fixed URL instead

2. **`frontend/sidebar.js`**
   - Removed backend URL loading/saving logic
   - Removed backend URL validation
   - Removed backend URL check before sending messages

3. **`frontend/sidebar.html`**
   - Removed backend URL input field from settings panel

4. **`frontend/manifest.json`**
   - Updated `host_permissions` to only your backend URL

---

## Before Deploying

### Step 1: Deploy Your Backend
Deploy your backend to a hosting service (Railway, Render, Fly.io, etc.) and get your HTTPS URL.

See `backend/DEPLOYMENT.md` for deployment guides.

### Step 2: Update Backend URL
In `frontend/background.js`, update:
```javascript
const BACKEND_URL = 'https://your-actual-backend-url.com';
```

### Step 3: Update Manifest
In `frontend/manifest.json`, update:
```json
"host_permissions": [
  "https://your-actual-backend-url.com/*"
]
```

**Important:** Make sure the URL matches exactly (including protocol and trailing `/*`).

### Step 4: Test Locally
1. Load the extension unpacked
2. Test that API calls work
3. Verify no CORS errors in console

### Step 5: Package and Submit
```bash
cd frontend
zip -r ../sidebar-scholar-extension.zip . -x "*.DS_Store"
```

---

## Understanding Permissions

### `host_permissions` vs `content_scripts.matches`

These are **different** and serve different purposes:

| Permission | Purpose | Your Value |
|------------|---------|------------|
| `host_permissions` | Allows fetch/XHR requests FROM extension TO these URLs | `"https://your-backend.com/*"` |
| `content_scripts.matches` | Determines which web pages the content script runs ON | `"<all_urls>"` |

**Why both?**

- `host_permissions`: Restricts API calls to only your backend ✅
- `content_scripts.matches`: Allows extracting content from any webpage (needed for functionality) ✅

This is the **correct** setup - you can read any page (for context) but only communicate with your backend.

---

## Chrome Web Store Justification

When submitting, justify `host_permissions` like this:

> **host_permissions: `https://your-backend.com/*`**
> 
> Required to make API requests to our backend server. The extension sends page context and user questions to our backend, which processes them using AI services. This is the only external server the extension communicates with.

And justify `content_scripts.matches`:

> **content_scripts.matches: `<all_urls>`**
> 
> Required to extract page content (title, text, headings) from any webpage the user visits. This content is only accessed when the user actively opens the sidebar and asks a question. The extension is designed to work on any website, not just specific domains.

---

## Rollback Plan

If you need to allow user-configurable backends again:

1. Revert changes to `background.js`, `sidebar.js`, `sidebar.html`
2. Change `host_permissions` back to `["https://*/*", "http://*/*"]`
3. Add backend URL input back to settings

**Note:** This will require broader permissions and longer Chrome Store review.

---

## Questions?

- **Q: Can users still use their own API keys?**  
  A: Yes! The API key override setting is still available.

- **Q: What if my backend URL changes?**  
  A: You'll need to update the extension and submit a new version.

- **Q: Can I support both fixed and custom backends?**  
  A: Technically yes, but it defeats the security benefits. Not recommended.

- **Q: What about localhost for development?**  
  A: You can temporarily change `BACKEND_URL` to `http://localhost:3000` for local testing, but remember to change it back before packaging for Chrome Store.



