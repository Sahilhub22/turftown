// ── TurfTown Main JS ──

document.addEventListener('DOMContentLoaded', () => {

  // ── Mobile Nav Toggle ──
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
      }
    });
  }

  // ── User Dropdown ──
  const userMenuBtn  = document.getElementById('userMenuBtn');
  const userDropdown = document.getElementById('userDropdown');
  if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('open');
    });
    document.addEventListener('click', () => {
      userDropdown.classList.remove('open');
    });
  }

  // ── Auto-dismiss flash messages ──
  setTimeout(() => {
    document.querySelectorAll('.flash').forEach(el => {
      el.style.animation = 'slideOutFlash 0.4s ease forwards';
      setTimeout(() => el.remove(), 400);
    });
  }, 5000);

  // ── Turf card hover sound effect (visual feedback) ──
  document.querySelectorAll('.turf-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.willChange = 'transform';
    });
    card.addEventListener('mouseleave', function() {
      this.style.willChange = 'auto';
    });
  });

  // ── Animate stats on scroll ──
  const statsItems = document.querySelectorAll('.admin-stat-num');
  if (statsItems.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    statsItems.forEach(el => observer.observe(el));
  }

  function animateCount(el) {
    const rawText = el.textContent;
    const numMatch = rawText.match(/[\d,]+/);
    if (!numMatch) return;
    const endVal = parseInt(numMatch[0].replace(/,/g, ''));
    if (isNaN(endVal) || endVal === 0) return;
    const prefix = rawText.startsWith('₹') ? '₹' : '';
    const duration = 800;
    const startTime = performance.now();
    const update = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(endVal * eased);
      el.textContent = prefix + current.toLocaleString('en-IN');
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = rawText;
    };
    el.textContent = prefix + '0';
    requestAnimationFrame(update);
  }

  // ── Scroll reveal for venue cards ──
  const revealCards = document.querySelectorAll('.turf-card, .why-card, .admin-stat-card');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, i * 40);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  revealCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    revealObserver.observe(card);
  });

  // ── Sport cards interactive highlight ──
  document.querySelectorAll('.sport-card').forEach(card => {
    card.addEventListener('click', function() {
      document.querySelectorAll('.sport-card').forEach(c => c.classList.remove('active-sport-card'));
      this.classList.add('active-sport-card');
    });
  });

  // ── Booking page: payment option toggle ──
  document.querySelectorAll('.payment-option').forEach(opt => {
    opt.addEventListener('click', function() {
      document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected-payment'));
      this.classList.add('selected-payment');
      const radio = this.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

});

// Slide out animation (CSS helper)
const styleEl = document.createElement('style');
styleEl.textContent = `
@keyframes slideOutFlash {
  to { transform: translateX(100%); opacity: 0; }
}`;
document.head.appendChild(styleEl);
