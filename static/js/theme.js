// Theme switcher with localStorage persistence
(function () {
  'use strict';
  
  const getStoredTheme = () => localStorage.getItem('ecopulse_theme');
  const setStoredTheme = theme => localStorage.setItem('ecopulse_theme', theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const setTheme = function (theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    const icon = document.getElementById('theme-icon');
    const mobileIcon = document.getElementById('mobile-theme-icon');
    const iconClass = theme === 'dark' ? 'fas fa-sun text-warning' : 'fas fa-moon text-secondary';
    if (icon) icon.className = iconClass;
    if (mobileIcon) mobileIcon.className = iconClass;
  };

  // Initial load
  setTheme(getPreferredTheme());

  window.addEventListener('DOMContentLoaded', () => {
    setTheme(getPreferredTheme());
    const toggleTheme = () => {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setStoredTheme(newTheme);
      setTheme(newTheme);
      window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
    };

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) toggleBtn.addEventListener('click', toggleTheme);

    const mobileToggleBtn = document.getElementById('mobile-theme-toggle-btn');
    if (mobileToggleBtn) mobileToggleBtn.addEventListener('click', toggleTheme);
  });
})();
