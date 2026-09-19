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
    if (icon) {
      if (theme === 'dark') {
        icon.className = 'fas fa-sun text-warning';
      } else {
        icon.className = 'fas fa-moon text-secondary';
      }
    }
  };

  // Initial load
  setTheme(getPreferredTheme());

  window.addEventListener('DOMContentLoaded', () => {
    setTheme(getPreferredTheme());
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setStoredTheme(newTheme);
        setTheme(newTheme);
        
        // Dispatch event for charts to re-render colors if needed
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
      });
    }
  });
})();
