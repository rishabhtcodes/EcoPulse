# 🌍 EcoPulse India – Environmental Intelligence & Risk Map System

> **EcoPulse India** is an enterprise-grade Environmental Intelligence and Air Quality Monitoring platform built with Python, Django 6.x, Leaflet, and Chart.js. It delivers real-time atmospheric sensor feeds, high-resolution satellite reconnaissance, chemical burden calculations, multi-city comparative benchmarking, and automated public advisories across major Indian cities.

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green?logo=django)](https://djangoproject.com)
[![Open-Meteo](https://img.shields.io/badge/Live%20API-Open--Meteo-teal)](https://open-meteo.com)
[![Leaflet](https://img.shields.io/badge/Mapping-Leaflet%20%2B%20Esri-emerald)](https://leafletjs.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Key Highlights & Architecture

- **100% Open-Access & Public**: No authentication is required to explore all dashboards, interactive maps, pollutant breakdowns, city comparisons, and weather matrices. Authentication (classic + Google & GitHub OAuth) is completely optional for personalizing favorite cities and admin management.
- **Real-Time Live Atmospheric Telemetry**: Integrated directly with **Open-Meteo Air Quality & Weather API** (100% free, unlimited, no API keys required). Real-time hourly AQI (US EPA & European), PM2.5, PM10, NO₂, SO₂, CO, O₃, temperature, humidity, rainfall, and wind speed are fetched and cached on-the-fly.
- **High-Resolution Satellite Reconnaissance**: Dedicated orbital viewing port on city detail pages powered by **Leaflet** and **Esri World Imagery** with exact GPS coordinates and pulsing radar markers.
- **Executive Obsidian Glassmorphism**: Tailored for both Light Mode and High-Contrast Dark Mode featuring translucent frosted cards, specular highlights, and glowing telemetry pills.
- **Interactive Alerts Center**: Real-time notification bell calculating critical, high, and moderate environmental advisories across the national monitoring network with read/unread tracking via `localStorage`.

---

## 1. Project Directory Structure

```text
EcoPulse/
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── ecopulse/                   # Project Core & Configuration
│   ├── settings.py             # Installed apps, templates, static root, Asia/Kolkata timezone
│   ├── urls.py                 # Central URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── cities/                     # City App
│   ├── models.py               # City entity with slug, metro flag, coordinates, latest queries
│   ├── views.py                # City list with search/sort & detailed city breakdown
│   ├── urls.py                 # /cities/ and /cities/<slug>/
│   └── admin.py                # Admin registration with filters and search
│
├── pollution/                  # Pollution Analytics App
│   ├── models.py               # AirQuality & EnvironmentalAnalysis models (methods: get_risk_level, get_dominant_pollutant, calculate_environmental_score)
│   ├── views.py                # National rankings, pollutant chemical trajectories
│   ├── urls.py                 # /pollution/
│   └── admin.py
│
├── weather/                    # Meteorological Matrix App
│   ├── models.py               # Weather model with comfort index formula
│   ├── views.py                # National weather grid & historical progression
│   ├── urls.py                 # /weather/
│   └── admin.py
│
├── dashboard/                  # Main Analytics Engine
│   ├── views.py                # Dashboard index, multi-city compare, about page, live autocomplete API
│   ├── urls.py                 # /, /compare/, /about/, /api/search/
│   └── management/commands/
│       └── seed_data.py        # Realistic 14-day data generator for 12 major Indian cities
│
├── accounts/                   # Authentication & Personalization
│   ├── models.py               # UserProfile and FavoriteCity
│   ├── views.py                # Login, registration, profile, and AJAX favorite toggle
│   ├── urls.py                 # /accounts/login/, /accounts/register/, /accounts/profile/
│   └── forms.py                # Custom registration form
│
├── templates/                  # Reusable Django Templates with Inheritance
│   ├── base.html               # Sticky navbar, theme toggle, global search modal, footer
│   ├── 404.html                # Friendly fallback error template
│   ├── dashboard/
│   │   ├── index.html          # Hero, KPIs, Doughnut chart, Risk card, 14-day trend line
│   │   ├── compare.html        # Side-by-side card matrix & Bar chart comparison
│   │   └── about.html          # Academic disclaimer, formula breakdowns, parameters
│   ├── cities/
│   │   ├── list.html           # Grid cards with state filters and AQI sorting
│   │   └── detail.html         # Individual city deep dive with full chemistry & telemetry log
│   ├── pollution/
│   │   └── analytics.html      # National ranking table & multi-line pollutant trajectories
│   ├── weather/
│   │   └── index.html          # Weather telemetry, comfort index, dual-axis line charts
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       └── profile.html        # Bookmarked cities & preferences
│
└── static/
    ├── css/
    │   └── custom.css          # Design system, glassmorphism, glowing dark mode, animations
    └── js/
        ├── theme.js            # Dark/light mode switcher with localStorage persistence
        ├── charts.js           # Reusable Chart.js renderers (Doughnut, Line, Bar)
        └── main.js             # Live search debouncing & AJAX bookmarking
```

---

## 2. Key Commands for Setup and Execution

### Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Seed Realistic Sample Data
```bash
python manage.py seed_data
```
*Populates 12 Indian cities (Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Chandigarh, Lucknow, Shimla) with 14 days of historical air quality and weather telemetry (180+ records each).*
- **Admin account**: `admin` / `admin123`
- **Student demo account**: `student` / `student123`

### Run Development Server
```bash
python manage.py runserver
```
Visit the application in your browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 3. Implemented Features

1. **Environmental KPI Dashboard**:
   - Live KPI cards for AQI, PM2.5, PM10, Temperature, Humidity, and Eco Score.
   - Dynamic trend badges calculating difference and percentage variation against previous day.
2. **Dynamic Pollutant Composition Doughnut**:
   - Calculates relative contribution percentages dynamically from the database (`PM2.5`, `PM10`, `NO₂`, `SO₂`, `CO`, `O₃`).
3. **Automated Diagnostic & Advisory**:
   - Algorithmic determination of dominant pollutant based on CPCB standard ratios.
   - Severity-based actionable health advisories.
4. **Interactive Temporal Trend Chart (Chart.js)**:
   - Interactive line chart toggling between AQI, PM2.5, Temperature, and Humidity across 14 historical days.
5. **Multi-City Comparison Engine (`/compare/`)**:
   - Multi-select city picker comparing any selected cities side-by-side with bar charts.
6. **National Directory & Sorting (`/cities/`)**:
   - Glassmorphic card grid with search by name or state, filter by metropolitan category, and sort by AQI or Eco Score.
7. **City Deep Dive & Satellite Reconnaissance (`/cities/<slug>/`)**:
   - Dedicated high-resolution Leaflet satellite orbital viewport alongside executive telemetry stats, on-the-fly live Open-Meteo sync, and 7-day historical telemetry logs.
8. **Real-Time Live Telemetry Engine**:
   - Zero-configuration hourly atmospheric ingestion via Open-Meteo with on-demand refresh triggers and REST API endpoints (`/api/sync-city/<slug>/`).
9. **Alerts & Notification Center**:
   - Automated notification dropdown computing critical, high, and moderate hazard thresholds with unread counter badges and localStorage synchronization.
10. **Pollution Intelligence (`/pollution/`)**:
    - National ranking table from most polluted to cleanest with color-coded risk badges.
11. **Weather Center (`/weather/`)**:
    - Temperature, humidity, wind, rainfall, barometric pressure, and comfort index ratings.
12. **Dark & Light Mode**:
    - Modern obsidian glassmorphic theme with glowing environmental accent colors and `localStorage` persistence.

---

## 4. Top Viva / Assessment Questions & Answers

**Q1: How does the real-time live data fetching work without paid API keys?**
> **Answer**: EcoPulse uses Open-Meteo's open-access atmospheric endpoints (`dashboard/services.py`). By querying exact GPS coordinates, it parses real-time hourly US EPA AQI, PM2.5, PM10, CO, NO₂, SO₂, and microclimates on-the-fly and caches them in the Django database.

**Q2: How does the project determine the "Dominant Pollutant"?**
> **Answer**: In `AirQuality.get_dominant_pollutant()`, each pollutant concentration is normalized against its respective CPCB/NAAQS reference limit (e.g., PM2.5 / 60, PM10 / 100, NO₂ / 80, SO₂ / 80, CO / 2.0). The pollutant with the highest normalized ratio is dynamically identified as the dominant pollutant driving atmospheric deterioration.

**Q3: How is the Environmental Score calculated?**
> **Answer**: In `AirQuality.calculate_environmental_score()`, a transparent formula starts at base 100 and applies weighted penalties:
> `Score = 100 - [(AQI / 500) * 65 + min(35, (PM2.5 / 250) * 35)]`
> Higher AQI and PM2.5 values lower the score toward zero, while clean air approaches 100.

**Q4: How does the website support public access while also offering authentication?**
> **Answer**: All main views are 100% public without login requirements. Authentication (with support for Google and GitHub OAuth) is completely optional, used only for saving favorite cities to a user profile and accessing administrative panels.

---

## 5. Live Production Deployment

- **Live URL**: [https://ecopulse-7w2c.onrender.com](https://ecopulse-7w2c.onrender.com)
- **Continuous Deployment**: Connected to the GitHub repository `main` branch.
- **Keepalive Automation**: GitHub Actions workflow (`.github/workflows/keepalive.yml`) pings the health endpoint every 10 minutes to prevent container sleep.

