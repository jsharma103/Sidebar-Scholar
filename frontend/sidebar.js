// Sidebar Scholar - Main UI Logic

let currentTabId = null;
let pageContext = null;
let isProcessingSelectedText = false; // Prevent duplicate processing

// Initialize sidebar
document.addEventListener('DOMContentLoaded', async () => {
  // Get current tab
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  currentTabId = tabs[0]?.id;

  // Load settings
  await loadSettings();

  // Load page context
  await loadPageContext();

  // Setup event listeners
  setupEventListeners();

  // Set up listener for storage changes (when new text is selected)
  // This is the primary way we receive selected text
  const storageListener = async (changes, areaName) => {
    if (areaName === 'local' && changes.pendingSelectedText) {
      const newText = changes.pendingSelectedText.newValue;
      if (newText && !isProcessingSelectedText) {
        isProcessingSelectedText = true;
        // Get the autoSend flag
        const result = await chrome.storage.local.get(['pendingAutoSend']);
        const autoSend = result.pendingAutoSend || false;
        console.log('Received selected text via storage listener:', newText, 'autoSend:', autoSend);
        populateSelectedText(newText, autoSend);
        // Clear it after using
        await chrome.storage.local.remove(['pendingSelectedText', 'pendingSelectedTextTimestamp', 'pendingAutoSend']);
        // Reset flag after a delay
        setTimeout(() => { isProcessingSelectedText = false; }, 500);
      }
    }
  };
  chrome.storage.onChanged.addListener(storageListener);

  // Also check when sidebar becomes visible (in case it was already open)
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      setTimeout(() => checkForPendingSelectedText(), 100);
    }
  });

  // Check for pending selected text (from keyboard shortcut)
  // Poll multiple times to catch text that was stored before sidebar loaded
  checkForPendingSelectedText();
  setTimeout(() => checkForPendingSelectedText(), 100);
  setTimeout(() => checkForPendingSelectedText(), 300);
  setTimeout(() => checkForPendingSelectedText(), 600);
  setTimeout(() => checkForPendingSelectedText(), 1000);

  // Show welcome message
  showWelcomeMessage();
});

async function loadSettings() {
  const result = await chrome.storage.sync.get(['apiProvider', 'apiKey']);
  
  // Load API provider (optional)
  if (result.apiProvider) {
    document.getElementById('apiProvider').value = result.apiProvider;
  }
  
  // Load API key override (optional)
  if (result.apiKey) {
    document.getElementById('apiKey').value = result.apiKey;
  }
}

function setupEventListeners() {
  // Settings toggle
  document.getElementById('settingsBtn').addEventListener('click', () => {
    const panel = document.getElementById('settingsPanel');
    panel.classList.toggle('hidden');
  });

  // Save settings
  document.getElementById('saveSettings').addEventListener('click', async () => {
    const apiProvider = document.getElementById('apiProvider').value.trim();
    const apiKey = document.getElementById('apiKey').value.trim();

    // Build settings object (only include non-empty values)
    const settings = {};
    if (apiProvider) {
      settings.apiProvider = apiProvider;
    }
    if (apiKey) {
      settings.apiKey = apiKey;
    }

    await chrome.storage.sync.set(settings);

    document.getElementById('settingsPanel').classList.add('hidden');
    showError('Settings saved!', false);
    setTimeout(() => hideError(), 2000);
  });

  // Send message
  const sendBtn = document.getElementById('sendBtn');
  const messageInput = document.getElementById('messageInput');

  sendBtn.addEventListener('click', sendMessage);
  
  messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Auto-resize textarea
  messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
  });
}

async function loadPageContext() {
  if (!currentTabId) return;

  try {
    const response = await chrome.tabs.sendMessage(currentTabId, {
      action: 'getPageContext'
    });
    
    if (response && response.context) {
      pageContext = response.context;
    }
  } catch (error) {
    console.error('Error loading page context:', error);
  }
}

function showWelcomeMessage() {
  const messagesDiv = document.getElementById('messages');
  const welcomeMsg = createMessage('assistant', 
    '👋 Hi! I\'m Sidebar Scholar. I can help you understand this page, explain jargon, answer questions, and more. What would you like to know?'
  );
  messagesDiv.appendChild(welcomeMsg);
}

async function sendMessage() {
  const input = document.getElementById('messageInput');
  const message = input.value.trim();

  if (!message) return;

  // Add user message to UI
  addMessage('user', message);
  input.value = '';
  input.style.height = 'auto';

  // Show thinking indicator
  showThinking();

  try {
    // Send to background script for API call
    const response = await chrome.runtime.sendMessage({
      action: 'askQuestion',
      question: message,
      context: pageContext,
      tabId: currentTabId
    });

    hideThinking();

    if (response.error) {
      showError(response.error);
      return;
    }

    if (response.answer) {
      addMessage('assistant', response.answer);
    }
  } catch (error) {
    hideThinking();
    showError('Failed to get response. Please check your backend server is running and try again.');
    console.error('Error:', error);
  }
}

function addMessage(role, content) {
  const messagesDiv = document.getElementById('messages');
  const message = createMessage(role, content);
  messagesDiv.appendChild(message);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function createMessage(role, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  
  // Simple markdown-like formatting
  contentDiv.innerHTML = formatMessage(content);

  messageDiv.appendChild(contentDiv);
  return messageDiv;
}

function formatMessage(text) {
  // Escape HTML first
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Format code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  
  // Format inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Format links
  html = html.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
  
  // Format line breaks
  html = html.replace(/\n/g, '<br>');
  
  // Format lists (simple)
  html = html.replace(/^\* (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  return html;
}

function showThinking() {
  document.getElementById('thinking').classList.remove('hidden');
  document.getElementById('sendBtn').disabled = true;
}

function hideThinking() {
  document.getElementById('thinking').classList.add('hidden');
  document.getElementById('sendBtn').disabled = false;
}

function showError(message, isError = true) {
  const errorDiv = document.getElementById('errorMessage');
  errorDiv.textContent = message;
  errorDiv.className = isError ? 'error-message' : 'error-message';
  errorDiv.style.background = isError ? '#5a1d1d' : '#1d5a1d';
  errorDiv.style.color = isError ? '#ff6b6b' : '#6bff6b';
  errorDiv.classList.remove('hidden');
}

function hideError() {
  document.getElementById('errorMessage').classList.add('hidden');
}

async function checkForPendingSelectedText() {
  // Check if there's pending selected text from keyboard shortcut
  if (isProcessingSelectedText) return false;
  
  try {
    const result = await chrome.storage.local.get(['pendingSelectedText', 'pendingSelectedTextTimestamp', 'pendingAutoSend']);
    if (result.pendingSelectedText) {
      // Only use if it's recent (within last 15 seconds)
      const timestamp = result.pendingSelectedTextTimestamp || 0;
      const age = Date.now() - timestamp;
      if (age < 15000) {
        isProcessingSelectedText = true;
        const autoSend = result.pendingAutoSend || false;
        console.log('Found pending selected text:', result.pendingSelectedText, 'autoSend:', autoSend);
        populateSelectedText(result.pendingSelectedText, autoSend);
        // Clear it after using
        await chrome.storage.local.remove(['pendingSelectedText', 'pendingSelectedTextTimestamp', 'pendingAutoSend']);
        // Reset flag after a delay
        setTimeout(() => { isProcessingSelectedText = false; }, 500);
        return true; // Found and populated text
      } else {
        // Text is too old, clear it
        await chrome.storage.local.remove(['pendingSelectedText', 'pendingSelectedTextTimestamp', 'pendingAutoSend']);
      }
    }
  } catch (error) {
    console.error('Error checking for pending selected text:', error);
  }
  return false;
}

function populateSelectedText(text, autoSend = false) {
  const input = document.getElementById('messageInput');
  if (input && text) {
    console.log('Populating selected text:', text, 'autoSend:', autoSend);
    // Replace existing text (don't append)
    input.value = text;
    // Focus the input
    input.focus();
    // Auto-resize
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    // Scroll input into view
    input.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Auto-send if requested (with a small delay to ensure UI is ready)
    if (autoSend) {
      setTimeout(() => {
        console.log('Auto-sending message');
        sendMessage();
      }, 100);
    }
  } else {
    console.warn('Could not populate text - input not found or text empty');
  }
}
