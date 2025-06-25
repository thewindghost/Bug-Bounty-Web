function goBack() {
    if (document.referrer) {
      window.location.href = document.referrer;
    } else {
      window.history.back();
    }
  }