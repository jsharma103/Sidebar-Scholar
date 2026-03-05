// Background Service Worker - Handles API calls to backend server

// Fixed backend URL - production Render service
const BACKEND_URL = 'https://sidebar-scholar-1.onrender.com';

// Open sidebar when extension icon is clicked
chrome.action.onClicked.addListener(async (tab) => {
  await chrome.sidePanel.open({ tabId: tab.id });
});

// Handle keyboard shortcut command
chrome.commands.onCommand.addListener((command, tab) => {
  console.log('Command received:', command, 'Tab:', tab?.id);
  
  if ((command === 'ask-selected-text' || command === 'paste-selected-text') && tab?.id) {
    const autoSend = command === 'ask-selected-text';
    console.log('Handling command:', command, 'autoSend:', autoSend);
    
    // IMPORTANT: Open sidebar IMMEDIATELY before any async operations
    // to preserve user gesture context
    chrome.sidePanel.open({ tabId: tab.id })
      .then(() => {
        console.log('Sidebar opened successfully');
        handleSelectedTextCommand(tab, autoSend);
      })
      .catch(err => {
        console.error('Error opening sidebar:', err);
        // Still try to handle the text even if sidebar didn't open
        handleSelectedTextCommand(tab, autoSend);
      });
  }
});

async function handleSelectedTextCommand(tab, autoSend = false) {
  try {
    console.log('handleSelectedTextCommand called for tab:', tab.id, 'autoSend:', autoSend);

    // Get selected text from the page
    let selectedText = '';
    try {
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          return window.getSelection().toString().trim();
        }
      });
      selectedText = results[0]?.result || '';
      console.log('Selected text:', selectedText);
    } catch (scriptError) {
      console.log('Could not get selected text:', scriptError);
    }
    
    if (selectedText) {
      await handleSelectedTextFromPage(tab.id, selectedText, autoSend);
    }
    
  } catch (error) {
    console.error('Error handling selected text command:', error);
  }
}

async function handleSelectedTextFromPage(tabId, selectedText, autoSend = false) {
  try {
    console.log('Handling selected text from page:', selectedText, 'autoSend:', autoSend);
    
    // Store selected text and autoSend flag (only once)
    await chrome.storage.local.set({ 
      pendingSelectedText: selectedText,
      pendingSelectedTextTimestamp: Date.now(),
      pendingAutoSend: autoSend
    });
    
  } catch (error) {
    console.error('Error handling selected text from page:', error);
  }
}

// Handle messages from sidebar
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'askQuestion') {
    handleQuestion(request.question, request.context, request.tabId)
      .then(answer => sendResponse({ answer }))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Keep channel open for async response
  }
});

async function handleQuestion(question, context, tabId) {
  // Get settings (API provider and key only - backend URL is fixed)
  const settings = await chrome.storage.sync.get(['apiProvider', 'apiKey']);
  
  // Use fixed backend URL
  const backendUrl = BACKEND_URL;
  
  // Prepare request body matching backend QuestionRequest model
  const requestBody = {
    question: question,
    context: {
      title: context?.title || '',
      url: context?.url || '',
      text: context?.text || '',
      headings: context?.headings || [],
      timestamp: context?.timestamp || new Date().toISOString()
    }
  };
  
  // Add optional API provider if specified
  if (settings.apiProvider) {
    requestBody.api_provider = settings.apiProvider;
  }
  
  // Add optional API key override if specified
  if (settings.apiKey) {
    requestBody.api_key = settings.apiKey;
  }
  
  // Call backend API
  return await callBackendAPI(backendUrl, requestBody);
}

async function callBackendAPI(backendUrl, requestBody) {
  const apiUrl = `${backendUrl}/api/ask`;
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      // Try to parse error response
      let errorMessage = `Backend error: ${response.statusText}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        // If JSON parsing fails, use status text
      }
      
      // Provide helpful error messages
      if (response.status === 400) {
        throw new Error(`Invalid request: ${errorMessage}`);
      } else if (response.status === 502) {
        throw new Error(`Backend API error: ${errorMessage}. Check your backend server configuration.`);
      } else if (response.status === 0 || response.status === 503) {
        throw new Error(`Cannot connect to backend server at ${backendUrl}. Make sure the server is running.`);
      } else {
        throw new Error(errorMessage);
      }
    }

    const data = await response.json();
    
    // Backend returns: { answer, provider, timestamp }
    if (!data.answer) {
      throw new Error('Backend returned empty answer');
    }
    
    return data.answer;
  } catch (error) {
    // Handle network errors
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      throw new Error(`Cannot connect to backend server at ${backendUrl}. Make sure the server is running and accessible.`);
    }
    throw error;
  }
}
