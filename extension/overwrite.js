// source: https://stackoverflow.com/questions/9515704/use-a-content-script-to-access-the-page-context-variables-and-functions/9517879#9517879
function injectScript(func) {
  let actualCode = '(' + func + ')()';
  let script = document.createElement('script');
  script.textContent = actualCode;
  (document.head||document.documentElement).appendChild(script);
  script.remove();
}

injectScript(function() {
  let window = Object.create(window.location);
  Object.defineProperty(window, 'href', {
    set: function(value) { 
      console.log(value);
      window.location.href = value;
    },
    writeable: true
  });
});


// PopState
// https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
// https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onbeforeunload
