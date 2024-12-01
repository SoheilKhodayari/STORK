function addBackendRedirect() {
  const ul = document.getElementById("selection");
  const li = document.createElement("li");
  li.appendChild(document.createTextNode("Backend"));
  ul.append(li);
}

function addHTML5Redirect() {
  const ul = document.getElementById("selection");
  const li = document.createElement("li");
  li.appendChild(document.createTextNode("HTML5"));
  ul.append(li);
}

function addJavascriptRedirect() {
  const ul = document.getElementById("selection");
  const li = document.createElement("li");
  li.appendChild(document.createTextNode("Javascript"));
  ul.append(li);
}

function clearSelection() {
  const ul = document.getElementById("selection");
  ul.innerHTML = "";
}

function redirect(urls) {
  console.log("Called");
  const ul = document.getElementById("selection");

  // get redirection type list
  let selections = ul.getElementsByTagName("li");

  // do not redirect if no redirection type was selected
  if (selections.length ==  0) {
    return false;
  }

  // encode all partial redirection URLS in reverse order
  let encodedUrl = btoa(document.getElementById("url").value);
  for (let i = selections.length - 1; i > 0; i--) {
    const type = selections[i].textContent.toLowerCase();
    encodedUrl = btoa(urls[type] + encodedUrl)
  }
  // except the first in the list
  const type = selections[0].textContent.toLowerCase();
  encodedUrl = urls[type] + encodedUrl;

  console.log("Redirecting to: " + encodedUrl);

  // redirect
  window.location.assign(encodedUrl);
  return false;
}
