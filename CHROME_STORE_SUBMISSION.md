# Chrome Web Store Submission Guide

This document walks you through publishing Sidebar Scholar to the Chrome Web Store.

## Prerequisites

Before submitting, ensure you have:

- [ ] Google Developer account ($5 one-time registration fee)
- [ ] Privacy policy hosted at a public URL
- [ ] Extension icons (16x16, 48x48, 128x128)
- [ ] Screenshots (1280x800 or 640x400)
- [ ] Promotional images (optional but recommended)

---

## Step 1: Host Your Privacy Policy

Your privacy policy must be publicly accessible. Options:

### Option A: GitHub Pages (Free)
1. Go to your repo Settings → Pages
2. Enable GitHub Pages from main branch
3. Your privacy policy URL will be: `https://[username].github.io/Sidebar-Scholar/PRIVACY_POLICY`

### Option B: Google Sites (Free)
1. Create a site at sites.google.com
2. Copy the privacy policy content
3. Publish and get the URL

### Option C: Your Own Website
Host `PRIVACY_POLICY.md` on your domain

---

## Step 2: Prepare Store Assets

### Required Icons
Create these in the `frontend/icons/` folder:
- `icon16.png` - 16x16 pixels
- `icon48.png` - 48x48 pixels  
- `icon128.png` - 128x128 pixels

### Required Screenshots (at least 1)
- Size: 1280x800 or 640x400 pixels
- Show the extension in action
- Recommended: 3-5 screenshots showing different features

### Store Icon
- Size: 128x128 pixels (same as icon128.png)

### Promotional Images (Optional but Recommended)
- Small promo tile: 440x280 pixels
- Large promo tile: 920x680 pixels
- Marquee promo tile: 1400x560 pixels

---

## Step 3: Register as Chrome Developer

1. Go to: https://chrome.google.com/webstore/devconsole
2. Pay the $5 one-time registration fee
3. Complete your developer profile

---

## Step 4: Create Your Listing

### Basic Information

**Extension Name:** Sidebar Scholar

**Summary (132 characters max):**
```
AI-powered sidebar that helps you understand any webpage. Ask questions, get explanations, and learn without leaving your tab.
```

**Description (16,000 characters max):**
```
🎓 Sidebar Scholar - Your AI Reading Companion

Sidebar Scholar brings powerful AI assistance directly to your browser. Understand complex articles, learn new concepts, and get instant explanations - all without leaving the page you're reading.

✨ KEY FEATURES

• 🤖 AI-Powered Answers: Get intelligent responses about any webpage content
• 📄 Context-Aware: Automatically understands the page you're viewing
• 💬 Sidebar Chat: Clean interface that doesn't interrupt your reading
• ⌨️ Keyboard Shortcuts: Quick access with Cmd+Shift+S (Mac) or Ctrl+Shift+S
• 🔒 Privacy-First: Your API keys stay local, data isn't stored

🚀 HOW IT WORKS

1. Click the extension icon to open the sidebar
2. Ask any question about the current page
3. Get an AI-generated answer with relevant context

📚 PERFECT FOR

• Students researching topics online
• Professionals reading technical documentation
• Anyone wanting to understand complex content
• Researchers analyzing articles

🔐 PRIVACY & SECURITY

• API keys stored locally in your browser only
• Page content sent only when you ask a question
• No browsing history or personal data collected
• All communications encrypted via HTTPS

⚙️ REQUIREMENTS

• Your own API key from OpenAI or Anthropic
• Chrome browser (version 116 or higher for side panel support)

📖 GETTING STARTED

1. Install the extension
2. Click the extension icon
3. Open settings (⚙️) and enter your API key
4. Start asking questions!

💡 EXAMPLE QUESTIONS

• "What is this article about?"
• "Explain [technical term] in simple terms"
• "Summarize the main points"
• "What are the key takeaways?"

---

Sidebar Scholar is open source and community-driven. We welcome feedback and contributions!

Support: [Your support link or email]
```

**Category:** Productivity

**Language:** English

---

## Step 5: Privacy Practices Questionnaire

When you upload your extension, Chrome will ask about data practices. Here's how to answer:

### "Does your extension collect user data?"
**Answer:** Yes

### "Which types of personal data does your extension collect?"

Check these boxes:
- [x] **Website content** - We read page content to provide context
- [x] **User activity** - We capture user questions and selected text

Do NOT check:
- [ ] Personally identifiable information
- [ ] Health information
- [ ] Financial and payment information
- [ ] Authentication information
- [ ] Personal communications
- [ ] Location
- [ ] Web history (we only access current page, not history)

### "How is this data used?"

Check these boxes:
- [x] **Functionality** - Core extension features

Do NOT check:
- [ ] Personalization
- [ ] Analytics
- [ ] Developer communications
- [ ] Advertising or marketing
- [ ] Credit decisions

### "Is the data sold to third parties?"
**Answer:** No

### "Is the data transferred to third parties?"
**Answer:** Yes

**Explain:** "Page content and user questions are sent to AI API providers (OpenAI or Anthropic) selected by the user to generate responses. No data is sold or used for advertising."

---

## Step 6: Permissions Justification

You MUST justify each permission. Here are the explanations:

### `activeTab`
```
Required to access the content of the current tab when the user opens the sidebar. This allows us to extract page context (title, text, URL) to provide relevant AI-powered answers. We only access the tab when the user actively uses the extension.
```

### `storage`
```
Required to save user preferences including: preferred AI provider, backend server URL, and API key. This ensures users don't need to re-enter settings each time they use the extension.
```

### `sidePanel`
```
Required to display the extension's main interface as a browser sidebar. This is the primary UI for interacting with the extension.
```

### `scripting`
```
Required to execute content scripts that extract page content and selected text. This enables the core functionality of understanding webpage content to answer user questions.
```

### `host_permissions` (all URLs)
```
Required to work on any website the user visits. Sidebar Scholar is a general-purpose reading assistant that should help users understand content on any webpage, not just specific sites. The extension only accesses page content when the user actively opens the sidebar and asks a question.
```

**⚠️ Note:** Broad host permissions may trigger additional review. Be prepared for follow-up questions from the Chrome team.

---

## Step 7: Upload and Submit

1. **Package your extension:**
   ```bash
   cd Sidebar-Scholar/frontend
   zip -r ../sidebar-scholar-extension.zip . -x "*.DS_Store"
   ```

2. **Upload to Developer Console:**
   - Go to: https://chrome.google.com/webstore/devconsole
   - Click "New Item"
   - Upload the .zip file

3. **Fill in all fields** (as described above)

4. **Submit for review**

---

## Step 8: Review Process

### Timeline
- Initial review: 1-3 business days (simple extensions)
- Extended review: 1-2 weeks (extensions with broad permissions)

### Common Rejection Reasons

1. **Missing or inaccessible privacy policy**
   - Ensure your privacy policy URL works
   - Make sure it's publicly accessible (not behind login)

2. **Unjustified permissions**
   - Provide clear explanations for each permission
   - Consider if you can reduce permissions

3. **Misleading description**
   - Be accurate about features
   - Don't overstate capabilities

4. **Policy violations**
   - No crypto mining
   - No deceptive behavior
   - No unauthorized data collection

### If Rejected
- Read the rejection reason carefully
- Make required changes
- Resubmit with a note explaining your fixes

---

## Post-Publication

### Monitoring
- Check developer console regularly
- Respond to user reviews
- Monitor for issues

### Updates
1. Increment version in `manifest.json`
2. Create new .zip package
3. Upload to developer console
4. Submit for review

---

## Checklist Before Submission

- [ ] Privacy policy hosted and accessible
- [ ] Icons created (16, 48, 128 px)
- [ ] Screenshots prepared
- [ ] manifest.json version is correct
- [ ] All files included in zip
- [ ] Extension tested and working
- [ ] Description written
- [ ] Permission justifications prepared
- [ ] $5 developer fee paid



