// Detect 3XX redirections
chrome.webRequest.onBeforeRedirect.addListener(
  function(details) {
    console.log("3XX redirection:");
    console.log("from: " + details.url);
    console.log("to: " + details.redirectUrl);
  },
  { urls: [ "<all_urls>" ] },
);

// Callback to handle redirections detected via content script
chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    // Used to detect HTML5 redirections
    if (request.type === "meta") {
      console.log("HTML5 redirection: ");
      console.log("from: " + request.sourceUrl);
      console.log("to: " + request.redirectUrl);
    }
    // Callback to handle unknown redirection (likely javascript)
    else if (request.type === "unknown") {
      console.log("Unknown redirection: ");
      console.log("from: " + request.sourceUrl);
      console.log("to: " + request.redirectUrl);
    }
  }
);
