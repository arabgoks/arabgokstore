function showToast(title, message, type = 'normal', duration = 3000) {
  const el = document.getElementById('toast-component');
  const titleEl = document.getElementById('toast-title');
  const msgEl = document.getElementById('toast-message');
  if (!el) return;

  // reset style
  el.classList.remove(
    'bg-white','text-gray-900','border-gray-300',
    'bg-green-50','text-green-700','border-green-400',
    'bg-red-50','text-red-700','border-red-400'
  );

  // set style by type
  if (type === 'success') {
    el.classList.add('bg-green-50','text-green-700','border-green-400');
  } else if (type === 'error') {
    el.classList.add('bg-red-50','text-red-700','border-red-400');
  } else {
    el.classList.add('bg-white','text-gray-900','border-gray-300'); // normal/info
  }

  // set content
  titleEl.textContent = title || 'ArabgokStore';
  msgEl.textContent = message || '';

  // show
  el.classList.remove('opacity-0','translate-y-16');
  el.classList.add('opacity-100','translate-y-0');

  // auto hide
  setTimeout(() => {
    el.classList.remove('opacity-100','translate-y-0');
    el.classList.add('opacity-0','translate-y-16');
  }, duration);
}