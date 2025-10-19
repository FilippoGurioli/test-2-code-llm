document.addEventListener("DOMContentLoaded", function() {
  if (typeof renderMathInElement !== 'function') {
    // auto-render not loaded
    return;
  }
  renderMathInElement(document.body, {
    // delimiters consistent with pymdownx.arithmatex generic output
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false},
    ],
    // don't throw on unknown commands (keeps pages robust)
    throwOnError: false
  });
});
