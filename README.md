# EcoPulse India – Project Walkthrough & Viva Guide

**EcoPulse India** is an Environmental Intelligence and City Pollution Monitoring platform built with Python and Django 6.x. It delivers real-time atmospheric diagnostics, dynamic chemical burden calculations, multi-city comparative benchmarking, and predictive public advisories across major Indian cities.

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
   - Search by name or state, filter by metropolitan category, sort by AQI or Eco Score.
7. **City Deep Dive (`/cities/<slug>/`)**:
   - Full chemical breakdown, microclimate stats, coordinates, and 7-day historical telemetry log.
8. **Pollution Intelligence (`/pollution/`)**:
   - National ranking table from most polluted to cleanest with color-coded risk badges.
9. **Weather Center (`/weather/`)**:
   - Temperature, humidity, wind, rainfall, barometric pressure, and comfort index ratings.
10. **Global Autocomplete Search**:
    - Real-time debounced search bar querying both city names and states.
11. **Dark & Light Mode**:
    - Modern glassmorphic theme with glowing environmental accent colors and `localStorage` persistence.
12. **Authentication & Bookmarking**:
    - Registration, login, profile view, and AJAX favorite city toggling.

---

## 4. Top Viva / Assessment Questions & Answers

**Q1: How does the project determine the "Dominant Pollutant"?**
> **Answer**: In `AirQuality.get_dominant_pollutant()`, each pollutant concentration is normalized against its respective CPCB/NAAQS reference limit (e.g., PM2.5 / 60, PM10 / 100, NO₂ / 80, SO₂ / 80, CO / 2.0). The pollutant with the highest normalized ratio is dynamically identified as the dominant pollutant driving atmospheric deterioration.

**Q2: How is the Environmental Score calculated?**
> **Answer**: In `AirQuality.calculate_environmental_score()`, a transparent formula starts at base 100 and applies weighted penalties:
> `Score = 100 - [(AQI / 500) * 65 + min(35, (PM2.5 / 250) * 35)]`
> Higher AQI and PM2.5 values lower the score toward zero, while clean air approaches 100.

**Q3: How are Django ORM relationships utilized in this project?**
> **Answer**:
> - `ForeignKey`: Links `AirQuality` and `Weather` records to a `City` with `on_delete=models.CASCADE` and `related_name`.
> - `OneToOneField`: Connects `EnvironmentalAnalysis` directly to a specific `AirQuality` record.
> - `ManyToMany / Junction`: Implemented through `FavoriteCity` linking `User` and `City`.

**Q4: How does the front-end handle real-time metric switching without full page reloads?**
> **Answer**: Chart data is serialized as JSON in Django views and injected into the template. The JavaScript module `EcoCharts` updates Chart.js dataset objects dynamically when metric pill buttons (`AQI`, `PM2.5`, `Temp`) are clicked.

**Q5: What security practices are followed?**
> **Answer**: CSRF protection on all forms via `{% csrf_token %}`, password hashing via Django PBKDF2 authentication, SQL injection prevention via Django ORM parameterized queries, and sanitized user inputs.
