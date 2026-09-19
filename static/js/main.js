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
});
