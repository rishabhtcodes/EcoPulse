// EcoPulse Global Interactivity
document.addEventListener('DOMContentLoaded', function() {
  // Global quick city search autocomplete
  const searchInput = document.getElementById('global-city-search');
  const searchDropdown = document.getElementById('global-search-results');

  if (searchInput && searchDropdown) {
    let debounceTimer;
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      const query = this.value.trim();
      if (query.length < 2) {
        searchDropdown.style.display = 'none';
        searchDropdown.innerHTML = '';
        return;
      }

      debounceTimer = setTimeout(() => {
        fetch(`/api/search/?term=${encodeURIComponent(query)}`)
          .then(res => res.json())
          .then(data => {
            searchDropdown.innerHTML = '';
            if (data.length === 0) {
              searchDropdown.innerHTML = '<div class="p-3 text-center text-muted small"><i class="fas fa-info-circle me-1"></i>No matching Indian cities found</div>';
              searchDropdown.style.display = 'block';
              return;
            }

            data.forEach(item => {
              const a = document.createElement('a');
              a.className = 'search-item';
              a.href = `/cities/${item.slug}/`;
              a.innerHTML = `
                <div>
                  <strong>${item.name}</strong>, <span class="text-muted small">${item.state}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                  <span class="badge" style="background-color: ${item.risk_color}">${item.risk}</span>
                  <span class="fw-bold small">AQI ${item.aqi}</span>
                </div>
              `;
              searchDropdown.appendChild(a);
            });
            searchDropdown.style.display = 'block';
          })
          .catch(err => console.error('Search error:', err));
      }, 250);
    });

    // Close on outer click
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.style.display = 'none';
      }
    });
  }

  // City Selector Quick Jump on Dashboard
  const citySelectJump = document.getElementById('dashboard-city-selector');
  if (citySelectJump) {
    citySelectJump.addEventListener('change', function() {
      if (this.value) {
        window.location.href = `/?city=${this.value}`;
      }
    });
  }

  // Favorite toggle AJAX
  document.querySelectorAll('.favorite-btn-ajax').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const cityId = this.dataset.cityId;
      fetch(`/accounts/favorite/toggle/${cityId}/`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          const icon = this.querySelector('i');
          if (data.favorited) {
            icon.className = 'fas fa-heart text-danger';
            this.title = 'Remove from favorites';
          } else {
            icon.className = 'far fa-heart text-muted';
            this.title = 'Add to favorites';
          }
        }
      })
      .catch(err => console.error('Favorite toggle failed', err));
    });
  });

  // ═══════════════════════════════════════════
  //  NOTIFICATION BELL SYSTEM
  // ═══════════════════════════════════════════
  const bellBtn    = document.getElementById('notif-bell-btn');
  const panel      = document.getElementById('notif-panel');
  const badge      = document.getElementById('notif-badge');
  const list       = document.getElementById('notif-list');
  const countPill  = document.getElementById('notif-count-pill');
  const markAllBtn = document.getElementById('notif-mark-read-btn');
  const updatedAt  = document.getElementById('notif-updated-at');

  if (!bellBtn || !panel) return;

  const READ_KEY = 'ep_notif_read_ids';

  function getReadIds() {
    try { return new Set(JSON.parse(localStorage.getItem(READ_KEY) || '[]')); }
    catch { return new Set(); }
  }
  function saveReadIds(ids) {
    localStorage.setItem(READ_KEY, JSON.stringify([...ids]));
  }

  // Severity helpers
  function getSeverity(aqi) {
    if (aqi > 300) return 'critical';
    if (aqi > 200) return 'high';
    if (aqi > 100) return 'moderate';
    return 'good';
  }
  function getSeverityIcon(sev) {
    return { critical: 'fa-skull-crossbones', high: 'fa-triangle-exclamation',
             moderate: 'fa-circle-exclamation', good: 'fa-circle-check' }[sev];
  }
  function getSeverityMsg(city, aqi, sev, dominant) {
    const msgs = {
      critical: `Hazardous air — AQI ${aqi}. ${dominant} at dangerous levels. Avoid all outdoor activity.`,
      high:     `Unhealthy air — AQI ${aqi}. ${dominant} elevated. Sensitive groups stay indoors.`,
      moderate: `Moderate pollution — AQI ${aqi}. ${dominant} slightly elevated. Limit strenuous outdoor activity.`,
      good:     `Air quality acceptable — AQI ${aqi}. ${dominant} within safe limits.`,
    };
    return msgs[sev];
  }

  let allAlerts = [];
  let panelOpen = false;

  function buildAlerts(cities) {
    // Only show Critical + High + notable Moderate alerts (AQI > 100)
    return cities
      .filter(c => c.aqi > 100)
      .sort((a, b) => b.aqi - a.aqi)
      .slice(0, 12)
      .map(c => ({
        id: `city-${c.id}`,
        name: c.name,
        state: c.state,
        slug: c.slug,
        aqi: c.aqi,
        dominant: c.dominant || 'PM2.5',
        severity: getSeverity(c.aqi),
      }));
  }

  function renderAlerts(alerts, readIds) {
    list.innerHTML = '';

    if (alerts.length === 0) {
      list.innerHTML = `
        <div class="notif-empty">
          <i class="fas fa-leaf"></i>
          All cities are within safe air quality limits
        </div>`;
      return;
    }

    alerts.forEach(a => {
      const isRead = readIds.has(a.id);
      const sev = a.severity;
      const icon = getSeverityIcon(sev);
      const msg  = getSeverityMsg(a.name, a.aqi, sev, a.dominant);

      const item = document.createElement('a');
      item.className = `notif-item${isRead ? '' : ' unread'}`;
      item.href = `/cities/${a.slug}/`;
      item.dataset.id = a.id;
      item.innerHTML = `
        <div class="notif-item-icon ${sev}">
          <i class="fas ${icon}"></i>
        </div>
        <div class="notif-item-body">
          <div class="notif-item-city">${a.name}, ${a.state}</div>
          <div class="notif-item-msg">${msg}</div>
        </div>
        <span class="notif-item-aqi ${sev}">AQI ${a.aqi}</span>
        ${isRead ? '' : '<span class="notif-unread-dot"></span>'}
      `;

      // Mark as read on click
      item.addEventListener('click', () => {
        const ids = getReadIds();
        ids.add(a.id);
        saveReadIds(ids);
      });

      list.appendChild(item);
    });
  }

  function updateBadge(alerts, readIds) {
    const unreadCount = alerts.filter(a => !readIds.has(a.id)).length;
    badge.textContent = unreadCount > 9 ? '9+' : unreadCount;
    badge.classList.toggle('zero', unreadCount === 0);
    countPill.textContent = `${unreadCount} unread`;
    countPill.classList.toggle('zero', unreadCount === 0);

    if (unreadCount > 0) {
      bellBtn.classList.add('has-alerts');
      // Pop animation
      badge.classList.add('pop');
      setTimeout(() => badge.classList.remove('pop'), 400);
    } else {
      bellBtn.classList.remove('has-alerts');
    }
  }

  function openPanel() {
    panel.classList.add('open');
    panelOpen = true;
    // Mark badge as seen (don't mark as read yet)
    bellBtn.classList.remove('has-alerts');
  }

  function closePanel() {
    panel.classList.remove('open');
    panelOpen = false;
  }

  // Toggle on bell click
  bellBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (panelOpen) closePanel(); else openPanel();
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (panelOpen && !panel.contains(e.target) && !bellBtn.contains(e.target)) {
      closePanel();
    }
  });

  // Mark all read
  markAllBtn && markAllBtn.addEventListener('click', () => {
    const ids = getReadIds();
    allAlerts.forEach(a => ids.add(a.id));
    saveReadIds(ids);
    renderAlerts(allAlerts, ids);
    updateBadge(allAlerts, ids);
  });

  // Fetch live data from API
  function loadAlerts() {
    fetch('/api/dashboard-data/')
      .then(res => res.json())
      .then(data => {
        allAlerts = buildAlerts(data.cities || []);
        const readIds = getReadIds();
        renderAlerts(allAlerts, readIds);
        updateBadge(allAlerts, readIds);

        const now = new Date();
        if (updatedAt) {
          updatedAt.textContent = `Updated ${now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}`;
        }
      })
      .catch(() => {
        if (list) {
          list.innerHTML = '<div class="notif-loading"><i class="fas fa-wifi-slash me-2"></i>Could not fetch alerts</div>';
        }
      });
  }

  // Initial load + refresh every 5 minutes
  loadAlerts();
  setInterval(loadAlerts, 5 * 60 * 1000);

  // Live Sync button logic
  const syncBtn = document.getElementById('btnSyncCity');
  const syncIcon = document.getElementById('syncIcon');
  if (syncBtn && syncIcon) {
    syncBtn.addEventListener('click', function () {
      const slug = this.getAttribute('data-slug');
      if (!slug) return;

      syncIcon.classList.add('fa-spin');
      fetch(`/api/sync-city/${slug}/`)
        .then(r => r.json())
        .then(data => {
          syncIcon.classList.remove('fa-spin');
          if (data.status === 'success') {
            // Update UI elements in city card
            const scoreVal = document.getElementById('cardScoreValue');
            if (scoreVal) scoreVal.innerHTML = `${data.aqi}<span class="fs-6 fw-normal text-muted">/500</span>`;

            const riskTier = document.getElementById('cardRiskTier');
            if (riskTier) riskTier.textContent = data.risk_level;

            const dominant = document.getElementById('cardDominant');
            if (dominant) dominant.textContent = data.dominant;

            const traffic = document.getElementById('cardTraffic');
            if (traffic) traffic.textContent = data.traffic;

            const temp = document.getElementById('cardTemp');
            if (temp) temp.textContent = `${data.temp}°C`;

            const rec = document.getElementById('cardRecommendation');
            if (rec && data.recommendation) rec.textContent = data.recommendation;

            // Flash badge to acknowledge live update
            const badge = document.getElementById('liveTelemetryBadge');
            if (badge) {
              badge.classList.remove('bg-success-subtle', 'text-success', 'border-success-subtle');
              badge.classList.add('bg-primary-subtle', 'text-primary', 'border-primary-subtle');
              setTimeout(() => {
                badge.classList.remove('bg-primary-subtle', 'text-primary', 'border-primary-subtle');
                badge.classList.add('bg-success-subtle', 'text-success', 'border-success-subtle');
              }, 1200);
            }

            // Refresh alert notifications
            loadAlerts();
          }
        })
        .catch(err => {
          syncIcon.classList.remove('fa-spin');
          console.warn('Real-time sync error:', err);
        });
    });
  }
});
