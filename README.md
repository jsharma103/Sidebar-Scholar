# Sidebar Scholar

A Chrome extension that brings AI-powered assistance directly to your browser sidebar. Ask questions about the current page, understand jargon, get explanations, and more - all without leaving your tab!

## Features

- 🤖 **AI-Powered Assistance**: Get intelligent answers about the current webpage
- 📄 **Page Context Awareness**: Automatically extracts and uses page content for context
- 💬 **Sidebar Interface**: Clean, modern UI that doesn't interrupt your browsing
- 🔒 **Privacy-Focused**: API keys stored locally, never shared
- ⚙️ **Flexible API Support**: Works with OpenAI, Anthropic (Claude), or custom APIs
- 🎨 **Cursor-like Design**: Beautiful dark theme inspired by modern IDEs

## Installation

### Option 1: Load as Unpacked Extension (Development)

1. Clone or download this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top-right corner)
4. Click "Load unpacked"
5. Select the `Sidebar-Scholar` folder
6. The extension icon should appear in your toolbar

### Option 2: Build from Source

```bash
cd Sidebar-Scholar
# No build step required - it's vanilla JavaScript!
```

## Setup

1. **Get an API Key**:
   - For OpenAI: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - For Anthropic: Get your API key from [Anthropic Console](https://console.anthropic.com/)
   - For Custom API: Configure your own API endpoint

2. **Configure the Extension**:
   - Click the Sidebar Scholar icon in your toolbar
   - Click the ⚙️ settings button
   - Enter your API key
   - Select your API provider
   - Click "Save Settings"

3. **Start Using**:
   - Click the extension icon to open the sidebar
   - Navigate to any webpage
   - Ask questions about the page content!

## Usage Examples

- **Understanding Content**: "What is this page about?"
- **Explaining Jargon**: "What does 'quantum computing' mean in this context?"
- **Summarizing**: "Can you summarize the main points?"
- **Clarifying Concepts**: "Explain how this works in simple terms"
- **Finding Information**: "What are the key takeaways?"

## How It Works

1. **Content Extraction**: When you open the sidebar, the extension extracts the main content from the current page
2. **Context Building**: The page title, URL, text content, and structure are gathered
3. **AI Processing**: Your question is sent along with the page context to your chosen AI API
4. **Response Display**: The AI's answer is displayed in the sidebar chat interface

## File Structure

```
Sidebar-Scholar/
├── manifest.json       # Extension configuration
├── sidebar.html        # Sidebar UI structure
├── sidebar.css         # Styling
├── sidebar.js          # Sidebar logic and UI interactions
├── content.js          # Content script for page extraction
├── background.js       # Service worker for API calls
├── icons/              # Extension icons (create these)
└── README.md           # This file
```

## Creating Icons

You'll need to create icon files for the extension. Create an `icons` folder and add:

- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

You can use any image editor or online tool to create these. A simple "S" or book icon works well!

Alternatively, you can use a placeholder service or generate icons using:
- [Favicon Generator](https://favicon.io/)
- [RealFaviconGenerator](https://realfavicongenerator.net/)

## API Providers

### OpenAI
- Model: `gpt-4o-mini` (cost-effective)
- Endpoint: `https://api.openai.com/v1/chat/completions`
- Get API key: [OpenAI Platform](https://platform.openai.com/api-keys)

### Anthropic (Claude)
- Model: `claude-3-haiku-20240307` (fast and affordable)
- Endpoint: `https://api.anthropic.com/v1/messages`
- Get API key: [Anthropic Console](https://console.anthropic.com/)

### Custom API
- Configure your own OpenAI-compatible API endpoint
- Useful for self-hosted models or other providers

## Privacy & Security

- ✅ API keys are stored locally using Chrome's sync storage
- ✅ No data is sent to third parties except your chosen API provider
- ✅ Page content is only sent when you ask a question
- ✅ All communication is encrypted via HTTPS
- ✅ No browsing history, personal info, or analytics collected

For complete details, see our [Privacy Policy](PRIVACY_POLICY.md).

## Troubleshooting

### Sidebar won't open
- Make sure you've clicked the extension icon in the toolbar
- Check that the extension is enabled in `chrome://extensions/`

### API errors
- Verify your API key is correct
- Check that you have API credits/quota available
- Ensure your API provider is selected correctly

### No page context
- Refresh the page and try again
- Some pages may block content scripts (try a different page)

### Extension not loading
- Make sure all files are in the correct directory
- Check the browser console for errors (`chrome://extensions/` → Details → Inspect views)

## Development

### Making Changes

1. Edit the relevant files
2. Go to `chrome://extensions/`
3. Click the refresh icon on the Sidebar Scholar extension
4. Test your changes

### Debugging

- **Sidebar**: Right-click extension icon → "Inspect popup" (or use sidebar context menu)
- **Content Script**: Use Chrome DevTools on the webpage
- **Background**: Go to `chrome://extensions/` → Details → "Inspect views: service worker"

## Future Enhancements

Potential features to add:
- [ ] Conversation history
- [ ] Export conversations
- [ ] Multiple model selection
- [ ] Custom prompts/templates
- [ ] Highlight text to ask questions
- [ ] Keyboard shortcuts
- [ ] Dark/light theme toggle

## License

MIT License - feel free to modify and use as you wish!

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

## Support

If you encounter any issues or have questions, please open an issue on the repository.

---

**Enjoy browsing with AI assistance! 🚀**



