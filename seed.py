import random
from app import create_app
from extensions import db
from models import User, Turf, TurfSlot, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import string

app = create_app()

FOOTBALL_TURFS = [
    ("KG Grass Football Arena", "KG Chavadi", "KG Chavadi"),
    ("RS Puram Football Ground", "RS Puram", "RS Puram"),
    ("Peelamedu Sports Hub", "Peelamedu", "Peelamedu"),
    ("Saibaba Colony Kick Arena", "Saibaba Colony", "Saibaba Colony"),
    ("Gandhipuram Goal Zone", "Gandhipuram", "Gandhipuram"),
    ("Singanallur Striker Park", "Singanallur", "Singanallur"),
    ("Vadavalli Victory Ground", "Vadavalli", "Vadavalli"),
    ("Hopes FC Turf", "Hope College Road", "Hope College"),
    ("Ondipudur Open Grounds", "Ondipudur", "Ondipudur"),
    ("Thudiyalur Thunder Arena", "Thudiyalur", "Thudiyalur"),
    ("Kovilpalayam Kick Zone", "Kovilpalayam", "Kovilpalayam"),
    ("Sundarapuram Sports City", "Sundarapuram", "Sundarapuram"),
    ("Sowripalayam Striker Hub", "Sowripalayam", "Sowripalayam"),
    ("Podanur Premier Ground", "Podanur", "Podanur"),
    ("Mettupalayam Football Elite", "Mettupalayam", "Mettupalayam"),
    ("Ukkadam United Ground", "Ukkadam", "Ukkadam"),
    ("Kuniyamuthur K-Zone", "Kuniyamuthur", "Kuniyamuthur"),
]

CRICKET_TURFS = [
    ("KG Turf Cricket Academy", "KG Chavadi", "KG Chavadi"),
    ("Race Course Cricket Park", "Race Course", "Race Course"),
    ("Peelamedu Premier Cricket", "Peelamedu", "Peelamedu"),
    ("Saibaba Colony Cricket Hub", "Saibaba Colony", "Saibaba Colony"),
    ("Gandhipuram Cricket Zone", "Gandhipuram", "Gandhipuram"),
    ("Singanallur Spin Arena", "Singanallur", "Singanallur"),
    ("Vadavalli Virat Ground", "Vadavalli", "Vadavalli"),
    ("PSG Cricket Net Zone", "Avinashi Road", "Avinashi Road"),
    ("Ondipudur Oval Ground", "Ondipudur", "Ondipudur"),
    ("Thudiyalur Cricket Elite", "Thudiyalur", "Thudiyalur"),
    ("Kovilpalayam Century Ground", "Kovilpalayam", "Kovilpalayam"),
    ("Sundarapuram Six Arena", "Sundarapuram", "Sundarapuram"),
    ("Sowripalayam Sixer Hub", "Sowripalayam", "Sowripalayam"),
    ("Podanur Pitch Perfect", "Podanur", "Podanur"),
    ("Neelambur Net Ground", "Neelambur", "Neelambur"),
    ("Ukkadam Cricket Academy", "Ukkadam", "Ukkadam"),
    ("Hopes Cricket Training Zone", "Hope College Road", "Hope College"),
    ("CODISSIA Cricket Grounds", "Avinashi Road", "Avinashi Road"),
]

BADMINTON_TURFS = [
    ("KG Shuttle Arena", "KG Chavadi", "KG Chavadi"),
    ("RS Puram Smash Zone", "RS Puram", "RS Puram"),
    ("Peelamedu Badminton Hub", "Peelamedu", "Peelamedu"),
    ("Saibaba Colony Court", "Saibaba Colony", "Saibaba Colony"),
    ("Gandhipuram Smash Arena", "Gandhipuram", "Gandhipuram"),
    ("Singanallur Shuttle Club", "Singanallur", "Singanallur"),
    ("Vadavalli Volley Shuttle", "Vadavalli", "Vadavalli"),
    ("Hope College Badminton", "Hope College Road", "Hope College"),
    ("Ondipudur Court Zone", "Ondipudur", "Ondipudur"),
    ("Thudiyalur Shuttle Hub", "Thudiyalur", "Thudiyalur"),
    ("Kovilpalayam Court Elite", "Kovilpalayam", "Kovilpalayam"),
    ("Sundarapuram Smash Club", "Sundarapuram", "Sundarapuram"),
    ("Sowripalayam Shuttle Court", "Sowripalayam", "Sowripalayam"),
    ("Podanur Premier Badminton", "Podanur", "Podanur"),
    ("Neelambur Net Zone", "Neelambur", "Neelambur"),
    ("Ukkadam Badminton Arena", "Ukkadam", "Ukkadam"),
    ("SITRA Shuttle Club", "Peelamedu", "Peelamedu"),
]

AMENITIES = [
    "Floodlights,Parking,Changing Room,Water,First Aid",
    "Floodlights,Parking,Restrooms,Cafeteria,Equipment Rental",
    "Parking,Changing Room,Water,Restrooms",
    "Floodlights,Parking,Changing Room,Cafeteria,Wi-Fi",
    "Floodlights,Parking,Water,First Aid,Equipment Rental",
    "Parking,Changing Room,Restrooms,First Aid",
    "Floodlights,Parking,Cafeteria,Wi-Fi,Changing Room,Restrooms",
]

DESCRIPTIONS = {
    'football': [
        "Premium artificial turf with FIFA-grade synthetic grass. Perfect for 5-a-side and 7-a-side matches.",
        "Well-maintained football ground with excellent drainage system. Floodlit for evening games.",
        "Top-quality football turf in the heart of Coimbatore. Book your slot now!",
        "Professional-grade turf ground ideal for tournaments, training sessions, and casual matches.",
    ],
    'cricket': [
        "Professionally laid cricket ground with a well-maintained pitch. Suitable for box cricket and net practice.",
        "Top-quality cricket turf with batting nets and full ground facilities.",
        "Box cricket arena with multiple pitches. Perfect for corporate tournaments and friendly matches.",
        "Well-maintained cricket ground with floodlights for day and night matches.",
    ],
    'badminton': [
        "Indoor synthetic court with international standard shuttle cock badminton court setup.",
        "Well-lit badminton court with premium synthetic flooring. Available for singles and doubles.",
        "Professional badminton court with anti-slip flooring and excellent lighting.",
        "Premium badminton facility with equipment rental available on-site.",
    ],
}

PRICES = {
    'football': [800, 900, 1000, 1100, 1200, 700, 750, 850, 950, 1050],
    'cricket': [600, 700, 800, 900, 1000, 550, 650, 750, 850, 950],
    'badminton': [200, 250, 300, 350, 400, 180, 220, 280, 320, 380],
}


def generate_ref():
    return 'TT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def seed_turfs():
    print("Seeding turfs...")

    all_turfs = []
    for name, location, area in FOOTBALL_TURFS:
        all_turfs.append({
            'name': name, 'location': location + ', Coimbatore', 'area': area,
            'sport_type': 'football',
            'price': random.choice(PRICES['football']),
            'description': random.choice(DESCRIPTIONS['football']),
            'amenities': random.choice(AMENITIES),
            'rating': round(random.uniform(3.8, 5.0), 1),
            'reviews': random.randint(20, 300),
        })
    for name, location, area in CRICKET_TURFS:
        all_turfs.append({
            'name': name, 'location': location + ', Coimbatore', 'area': area,
            'sport_type': 'cricket',
            'price': random.choice(PRICES['cricket']),
            'description': random.choice(DESCRIPTIONS['cricket']),
            'amenities': random.choice(AMENITIES),
            'rating': round(random.uniform(3.8, 5.0), 1),
            'reviews': random.randint(20, 300),
        })
    for name, location, area in BADMINTON_TURFS:
        all_turfs.append({
            'name': name, 'location': location + ', Coimbatore', 'area': area,
            'sport_type': 'badminton',
            'price': random.choice(PRICES['badminton']),
            'description': random.choice(DESCRIPTIONS['badminton']),
            'amenities': random.choice(AMENITIES),
            'rating': round(random.uniform(3.8, 5.0), 1),
            'reviews': random.randint(20, 300),
        })

    for t in all_turfs:
        turf = Turf(
            name=t['name'],
            location=t['location'],
            area=t['area'],
            city='Coimbatore',
            sport_type=t['sport_type'],
            price_per_hour=t['price'],
            description=t['description'],
            amenities=t['amenities'],
            rating=t['rating'],
            total_reviews=t['reviews'],
        )
        db.session.add(turf)

    db.session.commit()
    print(f"  [OK] Seeded {len(all_turfs)} turfs")


def seed_slots():
    print("Seeding slots for next 7 days...")
    turfs = Turf.query.all()
    today = datetime.now().date()
    slots_added = 0

    for turf in turfs:
        for day_offset in range(7):
            date = today + timedelta(days=day_offset)
            date_str = date.strftime('%Y-%m-%d')
            # Slots from 6am to 11pm, 1hr each
            for hour in range(6, 23):
                start = f"{hour:02d}:00"
                end = f"{hour+1:02d}:00"
                # Randomly book some slots (about 30%)
                is_booked = random.random() < 0.3
                slot = TurfSlot(
                    turf_id=turf.id,
                    date=date_str,
                    start_time=start,
                    end_time=end,
                    is_booked=is_booked,
                    price=turf.price_per_hour
                )
                db.session.add(slot)
                slots_added += 1

    db.session.commit()
    print(f"  [OK] Seeded {slots_added} slots")


def seed_admin():
    print("Creating admin user...")
    if not User.query.filter_by(email='admin@turftown.in').first():
        admin = User(
            name='TurfTown Admin',
            email='admin@turftown.in',
            phone='9000000000',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("  [OK] Admin created: admin@turftown.in / admin123")
    else:
        print("  [OK] Admin already exists")


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_admin()
        seed_turfs()
        seed_slots()
        print("\n[DONE] TurfTown database seeded successfully!")
        print(f"   Total turfs: {Turf.query.count()}")
        print(f"   Total slots: {TurfSlot.query.count()}")
