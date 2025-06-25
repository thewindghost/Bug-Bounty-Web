document.getElementById('settings-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const data = {
      email: document.getElementById('email').value,
      birth_date: document.getElementById('birth_date').value,
      password: document.getElementById('password').value,
      setting: document.getElementById('setting').value,
    };

    localStorage.setItem('style', data.setting);

    const xmlPayload = `
      <?xml version="1.0" encoding="UTF-8"?>
      <root>
        <email>${data.email}</email>
        <birth_date>${data.birth_date}</birth_date>
        <password>${data.password}</password>
        <setting>${data.setting}</setting>
      </root>
    `.trim();

    try {
      const res = await fetch('/user/setting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/xml' },
        credentials: 'include',
        body: xmlPayload
      });

      const html = await res.text();
      document.open();
      document.write(html);
      document.close();
    } catch (err) {
      document.getElementById('clientError').style.display = 'block';
      document.getElementById('clientError').textContent = "Failed to submit. Check network or server.";
    }
  });