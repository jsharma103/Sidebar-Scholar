// Content Script - Extracts page context

// Listen for messages from sidebar
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getPageContext') {
    const context = extractPageContext();
    sendResponse({ context });
  }
  return true; // Keep channel open for async response
});

function extractPageContext() {
  // Remove script and style elements
  const clone = document.cloneNode(true);
  const scripts = clone.querySelectorAll('script, style, noscript, iframe');
  scripts.forEach(el => el.remove());

  // Extract main content
  const title = document.title;
  const url = window.location.href;
  
  // Try to find main content areas
  const mainContent = findMainContent(clone);
  
  // Extract text content
  const textContent = mainContent ? mainContent.innerText : clone.body.innerText;
  
  // Clean up text
  const cleanedText = cleanText(textContent);
  
  // Extract headings for structure
  const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
    .slice(0, 10)
    .map(h => ({ level: h.tagName, text: h.innerText.trim() }))
    .filter(h => h.text.length > 0);

  return {
    title,
    url,
    text: cleanedText.substring(0, 8000), // Limit to ~8000 chars
    headings,
    timestamp: new Date().toISOString()
  };
}

function findMainContent(doc) {
  // Try common semantic elements
  const selectors = [
    'main',
    'article',
    '[role="main"]',
    '.content',
    '#content',
    '.main-content',
    '#main-content',
    '.post',
    '.article'
  ];

  for (const selector of selectors) {
    const element = doc.querySelector(selector);
    if (element) {
      return element;
    }
  }

  return doc.body;
}

function cleanText(text) {
  // Remove excessive whitespace
  return text
    .replace(/\s+/g, ' ')
    .replace(/\n\s*\n/g, '\n\n')
    .trim();
}
