// Chart.js helper module for EcoPulse
const EcoCharts = {
  getChartThemeColors: function() {
    const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    return {
      textColor: isDark ? '#94a3b8' : '#64748b',
      gridColor: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)',
      tooltipBg: isDark ? '#1e293b' : '#ffffff',
      tooltipText: isDark ? '#f8fafc' : '#0f172a',
      borderColor: isDark ? '#334155' : '#e2e8f0',
    };
  },

  renderPollutantDoughnut: function(canvasId, percentages) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const labels = Object.keys(percentages);
    const dataValues = Object.values(percentages);

    const colors = [
      '#ef4444', // PM2.5 (Crimson Red)
      '#f97316', // PM10 (Orange)
      '#eab308', // NO2 (Yellow)
      '#06b6d4', // SO2 (Cyan)
      '#8b5cf6', // CO (Purple)
      '#10b981', // O3 (Emerald Green)
    ];

    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: dataValues,
          backgroundColor: colors.slice(0, labels.length),
          borderWidth: 2,
          borderColor: document.documentElement.getAttribute('data-bs-theme') === 'dark' ? '#13222d' : '#ffffff',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
              color: document.documentElement.getAttribute('data-bs-theme') === 'dark' ? '#94a3b8' : '#64748b'
            }
          },
          tooltip: {
            callbacks: {
              label: function(item) {
                return ` ${item.label}: ${item.parsed}% relative load`;
              }
            }
          }
        }
      }
    });
  },

  renderTrendChart: function(canvasId, trendData, initialMetric = 'aqi') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const theme = EcoCharts.getChartThemeColors();

    const metricConfigs = {
      aqi: {
        label: 'Air Quality Index (AQI)',
        data: trendData.aqi,
        borderColor: '#f97316',
        backgroundColor: 'rgba(249, 115, 22, 0.15)',
        unit: ''
      },
      pm25: {
        label: 'PM2.5 (µg/m³)',
        data: trendData.pm25,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.15)',
        unit: ' µg/m³'
      },
      temp: {
        label: 'Temperature (°C)',
        data: trendData.temp,
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.15)',
        unit: '°C'
      },
      humidity: {
        label: 'Humidity (%)',
        data: trendData.humidity,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.15)',
        unit: '%'
      }
    };

    const activeConfig = metricConfigs[initialMetric] || metricConfigs.aqi;

    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: trendData.dates,
        datasets: [{
          label: activeConfig.label,
          data: activeConfig.data,
          borderColor: activeConfig.borderColor,
          backgroundColor: activeConfig.backgroundColor,
          borderWidth: 2.5,
          fill: true,
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: activeConfig.borderColor
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, font: { family: "'Plus Jakarta Sans', sans-serif" } }
          },
          y: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, font: { family: "'Plus Jakarta Sans', sans-serif" } }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            borderColor: theme.borderColor,
            borderWidth: 1,
            callbacks: {
              label: function(ctx) {
                return ` ${ctx.dataset.label}: ${ctx.parsed.y}`;
              }
            }
          }
        }
      }
    });

    // Helper to update metric
    chart.switchMetric = function(newMetric) {
      const cfg = metricConfigs[newMetric];
      if (!cfg) return;
      chart.data.datasets[0].label = cfg.label;
      chart.data.datasets[0].data = cfg.data;
      chart.data.datasets[0].borderColor = cfg.borderColor;
      chart.data.datasets[0].backgroundColor = cfg.backgroundColor;
      chart.data.datasets[0].pointBackgroundColor = cfg.borderColor;
      chart.update();
    };

    return chart;
  },

  renderComparisonBar: function(canvasId, compareData, metric = 'aqi') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    const theme = EcoCharts.getChartThemeColors();

    const colors = ['#0f766e', '#0d9488', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: compareData.labels,
        datasets: [{
          label: metric.toUpperCase(),
          data: compareData[metric],
          backgroundColor: colors.slice(0, compareData.labels.length),
          borderRadius: 8,
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: theme.textColor, font: { family: "'Plus Jakarta Sans', sans-serif" } }
          },
          y: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, font: { family: "'Plus Jakarta Sans', sans-serif" } }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            borderColor: theme.borderColor,
            borderWidth: 1
          }
        }
      }
    });
  }
};
