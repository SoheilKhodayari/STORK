function save_options() {
  console.log("save options called");
  let backend_url = document.getElementById("backend_url").value;
  chrome.storage.local.set({
    backend_url 
  }, function() {
    let stored = document.getElementById("stored"); 
    stored.appendChild(document.createTextNode(backend_url));
    stored.textContent = backend_url;
    console.log("New backend_url saved: " + backend_url);
  });
}

function restore_options() {
  chrome.storage.local.get({
    backend_url: "https://example.com"
  }, function(items) {
    document.getElementById("stored").textContent = items.backend_url
  });
}

document.addEventListener("DOMContentLoaded", restore_options);
document.getElementById("save").addEventListener("click", save_options);
