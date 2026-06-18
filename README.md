# 🏟️ TurfTown – Coimbatore's Biggest Turf Booking Platform

A full-featured turf booking management system built with **Python Flask + SQLite**, inspired by TurfTown.in. Book football, cricket, and badminton venues across Coimbatore instantly.

![TurfTown](static/images/football_player.png)

---

## ✨ Features

- 🔍 **Browse 52+ venues** across Coimbatore (Football, Cricket, Badminton)
- 📅 **Slot-based booking** — visual time grid (green = available, red = booked)
- 👤 **User authentication** — Register, Login, My Bookings
- 🔐 **Admin panel** — Manage turfs, bookings, dashboard stats
- 📍 **Filter by area, price, sport** with sidebar filters
- ⭐ **Ratings & reviews** display per venue
- 🌙 **Dark theme** inspired by TurfTown.in

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x + Flask 3 |
| Database | SQLite via SQLAlchemy |
| Auth | Flask-Login |
| Frontend | Vanilla HTML/CSS/JS |
| Styling | Custom dark theme CSS |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/turftown.git
cd turftown
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed the database (first time only)
```bash
python seed.py
```

### 4. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@turftown.in` | `admin123` |
| User | Register a new account | — |

---

## 📁 Project Structure

```
turfbook/
├── app.py              # Flask app factory
├── extensions.py       # SQLAlchemy & LoginManager instances
├── models.py           # Database models (User, Turf, Slot, Booking)
├── routes.py           # All route blueprints
├── seed.py             # Database seeder (52 turfs + slots)
├── requirements.txt
├── static/
│   ├── css/style.css   # Full dark theme CSS
│   ├── js/main.js      # Interactive JS
│   └── images/         # Sport card images
└── templates/
    ├── base.html
    ├── index.html       # Home page
    ├── venues.html      # Browse & filter
    ├── turf_detail.html # Slot picker
    ├── booking_confirm.html
    ├── booking_success.html
    ├── my_bookings.html
    ├── login.html
    ├── register.html
    └── admin/
        ├── dashboard.html
        ├── manage_turfs.html
        ├── add_turf.html
        └── manage_bookings.html
```

---

## 🌐 Pages

| URL | Description |
|-----|-------------|
| `/` | Home with hero, sport cards, featured venues |
| `/venues?sport=football` | All football grounds |
| `/venues?sport=cricket` | All cricket grounds |
| `/venues?sport=badminton` | All badminton courts |
| `/turf/<id>` | Turf detail + slot booking |
| `/my-bookings` | User's booking history |
| `/admin/` | Admin dashboard |

---

## 📍 Areas Covered in Coimbatore

KG Chavadi · RS Puram · Peelamedu · Saibaba Colony · Gandhipuram · Singanallur · Vadavalli · Ondipudur · Thudiyalur · Kovilpalayam · Sundarapuram · Sowripalayam · Podanur · Ukkadam · Neelambur · and more!

---

Made with ❤️ in Coimbatore
