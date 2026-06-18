from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import User, Turf, TurfSlot, Booking
from extensions import db
from datetime import datetime, timedelta
import random, string
from functools import wraps

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
booking = Blueprint('booking', __name__)
admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


# ─────────────────────────────────────────────
# Admin decorator
# ─────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────
# Main Routes
# ─────────────────────────────────────────────
@main.route('/')
def home():
    featured_football = Turf.query.filter_by(sport_type='football', is_active=True).order_by(Turf.rating.desc()).limit(6).all()
    featured_cricket = Turf.query.filter_by(sport_type='cricket', is_active=True).order_by(Turf.rating.desc()).limit(6).all()
    featured_badminton = Turf.query.filter_by(sport_type='badminton', is_active=True).order_by(Turf.rating.desc()).limit(6).all()
    total_turfs = Turf.query.filter_by(is_active=True).count()
    return render_template('index.html',
                           featured_football=featured_football,
                           featured_cricket=featured_cricket,
                           featured_badminton=featured_badminton,
                           total_turfs=total_turfs)


@main.route('/venues')
def venues():
    sport = request.args.get('sport', '')
    area = request.args.get('area', '')
    price_max = request.args.get('price_max', type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'rating')

    query = Turf.query.filter_by(is_active=True)

    if sport:
        query = query.filter_by(sport_type=sport)
    if area:
        query = query.filter(Turf.area.ilike(f'%{area}%'))
    if price_max:
        query = query.filter(Turf.price_per_hour <= price_max)
    if search:
        query = query.filter(
            (Turf.name.ilike(f'%{search}%')) |
            (Turf.location.ilike(f'%{search}%')) |
            (Turf.area.ilike(f'%{search}%'))
        )

    if sort == 'price_asc':
        query = query.order_by(Turf.price_per_hour.asc())
    elif sort == 'price_desc':
        query = query.order_by(Turf.price_per_hour.desc())
    else:
        query = query.order_by(Turf.rating.desc())

    turfs = query.all()

    football_count = Turf.query.filter_by(sport_type='football', is_active=True).count()
    cricket_count = Turf.query.filter_by(sport_type='cricket', is_active=True).count()
    badminton_count = Turf.query.filter_by(sport_type='badminton', is_active=True).count()

    areas = db.session.query(Turf.area).distinct().order_by(Turf.area).all()
    areas = [a[0] for a in areas]

    return render_template('venues.html',
                           turfs=turfs,
                           sport=sport,
                           area=area,
                           search=search,
                           sort=sort,
                           areas=areas,
                           football_count=football_count,
                           cricket_count=cricket_count,
                           badminton_count=badminton_count,
                           total=len(turfs))


@main.route('/turf/<int:turf_id>')
def turf_detail(turf_id):
    turf = Turf.query.get_or_404(turf_id)
    today = datetime.now().date()
    selected_date = request.args.get('date', today.strftime('%Y-%m-%d'))

    # Generate dates for next 7 days
    dates = []
    for i in range(7):
        d = today + timedelta(days=i)
        dates.append({'date': d.strftime('%Y-%m-%d'), 'label': d.strftime('%a, %d %b')})

    # Get slots for selected date
    slots = TurfSlot.query.filter_by(turf_id=turf_id, date=selected_date).order_by(TurfSlot.start_time).all()

    # If no slots exist for date, generate them
    if not slots:
        for hour in range(6, 23):
            slot = TurfSlot(
                turf_id=turf_id,
                date=selected_date,
                start_time=f"{hour:02d}:00",
                end_time=f"{hour+1:02d}:00",
                is_booked=False,
                price=turf.price_per_hour
            )
            db.session.add(slot)
        db.session.commit()
        slots = TurfSlot.query.filter_by(turf_id=turf_id, date=selected_date).order_by(TurfSlot.start_time).all()

    amenities_list = turf.amenities.split(',') if turf.amenities else []

    # Related turfs
    related = Turf.query.filter_by(sport_type=turf.sport_type, is_active=True)\
                        .filter(Turf.id != turf.id).limit(4).all()

    return render_template('turf_detail.html',
                           turf=turf,
                           slots=slots,
                           dates=dates,
                           selected_date=selected_date,
                           amenities_list=amenities_list,
                           related=related)


# ─────────────────────────────────────────────
# Auth Routes
# ─────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}! 🏟️', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not all([name, email, phone, password]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        user = User(name=name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account created! Welcome to TurfTown, {name}! 🎉', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.home'))


# ─────────────────────────────────────────────
# Booking Routes
# ─────────────────────────────────────────────
@booking.route('/book/<int:slot_id>', methods=['GET', 'POST'])
@login_required
def book_slot(slot_id):
    slot = TurfSlot.query.get_or_404(slot_id)
    turf = slot.turf

    if slot.is_booked:
        flash('This slot is already booked. Please choose another.', 'warning')
        return redirect(url_for('main.turf_detail', turf_id=turf.id))

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'Pay at Venue')
        ref = 'TT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        new_booking = Booking(
            user_id=current_user.id,
            turf_id=turf.id,
            slot_id=slot.id,
            total_price=slot.price,
            payment_method=payment_method,
            booking_ref=ref,
            status='confirmed'
        )
        slot.is_booked = True
        db.session.add(new_booking)
        db.session.commit()

        flash('🎉 Slot booked successfully!', 'success')
        return redirect(url_for('booking.booking_success', booking_id=new_booking.id))

    return render_template('booking_confirm.html', slot=slot, turf=turf)


@booking.route('/booking/success/<int:booking_id>')
@login_required
def booking_success(booking_id):
    b = Booking.query.get_or_404(booking_id)
    if b.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('booking_success.html', booking=b, turf=b.turf, slot=b.slot)


@booking.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id)\
                            .order_by(Booking.booking_date.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)


@booking.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    b = Booking.query.get_or_404(booking_id)
    if b.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('booking.my_bookings'))
    b.status = 'cancelled'
    b.slot.is_booked = False
    db.session.commit()
    flash('Booking cancelled successfully.', 'info')
    return redirect(url_for('booking.my_bookings'))


# ─────────────────────────────────────────────
# Admin Routes
# ─────────────────────────────────────────────
@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_bookings = Booking.query.count()
    today_bookings = Booking.query.filter(
        db.func.date(Booking.booking_date) == datetime.now().date()
    ).count()
    total_turfs = Turf.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    total_revenue = db.session.query(db.func.sum(Booking.total_price))\
                              .filter_by(status='confirmed').scalar() or 0

    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()

    sport_stats = {
        'football': Booking.query.join(Turf).filter(Turf.sport_type == 'football').count(),
        'cricket': Booking.query.join(Turf).filter(Turf.sport_type == 'cricket').count(),
        'badminton': Booking.query.join(Turf).filter(Turf.sport_type == 'badminton').count(),
    }

    return render_template('admin/dashboard.html',
                           total_bookings=total_bookings,
                           today_bookings=today_bookings,
                           total_turfs=total_turfs,
                           total_users=total_users,
                           total_revenue=total_revenue,
                           recent_bookings=recent_bookings,
                           sport_stats=sport_stats)


@admin_bp.route('/turfs')
@login_required
@admin_required
def manage_turfs():
    sport = request.args.get('sport', '')
    query = Turf.query
    if sport:
        query = query.filter_by(sport_type=sport)
    turfs = query.order_by(Turf.id.desc()).all()
    return render_template('admin/manage_turfs.html', turfs=turfs, sport=sport)


@admin_bp.route('/turfs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_turf():
    if request.method == 'POST':
        turf = Turf(
            name=request.form['name'],
            location=request.form['location'],
            area=request.form['area'],
            city=request.form.get('city', 'Coimbatore'),
            sport_type=request.form['sport_type'],
            price_per_hour=float(request.form['price_per_hour']),
            description=request.form.get('description', ''),
            amenities=request.form.get('amenities', ''),
            rating=float(request.form.get('rating', 4.0)),
            open_time=request.form.get('open_time', '06:00'),
            close_time=request.form.get('close_time', '23:00'),
        )
        db.session.add(turf)
        db.session.commit()
        flash(f'Turf "{turf.name}" added successfully!', 'success')
        return redirect(url_for('admin_bp.manage_turfs'))
    return render_template('admin/add_turf.html')


@admin_bp.route('/turfs/toggle/<int:turf_id>', methods=['POST'])
@login_required
@admin_required
def toggle_turf(turf_id):
    turf = Turf.query.get_or_404(turf_id)
    turf.is_active = not turf.is_active
    db.session.commit()
    status = 'activated' if turf.is_active else 'deactivated'
    flash(f'Turf "{turf.name}" {status}.', 'success')
    return redirect(url_for('admin_bp.manage_turfs'))


@admin_bp.route('/bookings')
@login_required
@admin_required
def manage_bookings():
    status_filter = request.args.get('status', '')
    query = Booking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    bookings = query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin/manage_bookings.html', bookings=bookings, status_filter=status_filter)


@admin_bp.route('/bookings/update/<int:booking_id>', methods=['POST'])
@login_required
@admin_required
def update_booking_status(booking_id):
    b = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    if new_status in ['confirmed', 'cancelled', 'completed']:
        if new_status == 'cancelled' and b.status != 'cancelled':
            b.slot.is_booked = False
        b.status = new_status
        db.session.commit()
        flash(f'Booking {b.booking_ref} updated to {new_status}.', 'success')
    return redirect(url_for('admin_bp.manage_bookings'))
