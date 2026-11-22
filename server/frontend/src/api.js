function cookie(name) {
  return document.cookie.split('; ').find((row) => row.startsWith(`${name}=`))?.split('=')[1];
}

export async function csrfFetch(url, options = {}) {
  if (!cookie('csrftoken')) await fetch('/djangoapp/csrf', { credentials: 'same-origin' });
  const headers = new Headers(options.headers || {});
  headers.set('X-CSRFToken', decodeURIComponent(cookie('csrftoken') || ''));
  return fetch(url, { ...options, headers, credentials: 'same-origin' });
}
