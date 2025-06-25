(function () {
    const style = localStorage.getItem('style') || 'light_mode';
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.onload = () => document.body.style.visibility = 'visible';
    link.href = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.head.appendChild(link);
  })();