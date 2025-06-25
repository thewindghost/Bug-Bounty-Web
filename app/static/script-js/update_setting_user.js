document.addEventListener('DOMContentLoaded', function() {
  document
    .getElementById('settings-form')
    .addEventListener('submit', async function(e) {
      e.preventDefault();

      // 1) Lưu theme mới ngay khi submit
      const setting = document.getElementById('setting').value;
      localStorage.setItem('style', setting);

      // 2) Tạo rồi gửi XML
      const xml = `
        <?xml version="1.0" encoding="UTF-8"?>
        <root>
          <email>${document.getElementById('email').value}</email>
          <birth_date>${document.getElementById('birth_date').value}</birth_date>
          <password>${document.getElementById('password').value}</password>
          <setting>${setting}</setting>
        </root>
      `.trim();

      try {
        const res = await fetch('/user/setting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/xml' },
          credentials: 'include',
          body: xml
        });
        if (!res.ok) throw new Error();

        // 3) Viết đè page mới
        const html = await res.text();
        document.open();
        document.write(html);
        document.close();

        // 4) Re-inject CSS theo localStorage
        const mode2 = localStorage.getItem('style') || 'light_mode';
        const href2 = mode2 === 'dark_mode'
          ? '/static/styles/style2.css'
          : '/static/styles/style1.css';
        const old = document.getElementById('theme-stylesheet');
        if (old) old.remove();
        const link = document.createElement('link');
        link.id = 'theme-stylesheet';
        link.rel = 'stylesheet';
        link.href = href2;
        document.head.appendChild(link);

      } catch {
        const box = document.getElementById('clientError');
        box.style.display = 'block';
        box.textContent = 'Failed to submit. Check network or server.';
      }
    });
});