// Detect HTML5 redirections
{
  let meta = document.head.querySelector("meta[http-equiv='refresh']");
  if (meta) {
    let content = meta.getAttribute("content");
    let redirectUrl = content.substring(content.indexOf("URL=") + 4);
    chrome.runtime.sendMessage(
      {
        type: "meta",
        sourceUrl: window.location.href,
        redirectUrl: redirectUrl
      }
    );
  }
}

// window.addEventListener("message", function(event) {
//   console.log("message received");
//   if (event.source != window) {
//     return;
//   }

//   if (event.data.type && (event.data.type == "UNKNOWN-REDIRECT")) {
//     chrome.runtime.sendMessage(
//       {
//         type: "unknow",
//         sourceUrl: window.location.href,
//         redirectUrl: "unknown"
//       }
//     );
//   }
// }, false);

// // Detect unknow redirection (likely javascript)
// window.addEventListener("beforeunload", function() {
//     console.log("beforeunload"); 
//     window.postMessage({
//       type: "UNKNOWN-REDIRECT",
//     }, "*");
// }, false);

// window.addEventListener("message", function(event) {
//   console.log("message received");
//   if (event.source != window) {
//     return;
//   }

//   if (event.data.type && (event.data.type == "UNKNOWN-REDIRECT")) {
//     chrome.runtime.sendMessage(
//       {
//         type: "unknow",
//         sourceUrl: window.location.href,
//         redirectUrl: "unknown"
//       }
//     );
//   }
// }, false);

