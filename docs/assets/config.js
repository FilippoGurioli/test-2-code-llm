window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
  },
  options: {
    skipHtmlTags: {
      'script': true,
      'noscript': true,
      'style': true,
      'pre': true
    }
  }
};
