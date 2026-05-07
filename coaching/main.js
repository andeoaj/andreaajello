/* ─────────────────────────────────────────────
   main.js — Andrea Ajello Coaching Website
───────────────────────────────────────────── */

// ─── Year in footer ───
document.getElementById('year').textContent = new Date().getFullYear();

// ─── Navbar: add 'scrolled' class on scroll ───
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// ─── Mobile hamburger menu ───
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.setAttribute('aria-expanded', isOpen);
});

// Close menu when a link is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// ─── Scroll fade-in animation ───
const fadeEls = document.querySelectorAll(
  '#about, #approach, #who, #offer, #contact, ' +
  '.card, .credential-item, .fit-list li, .offer-detail'
);

fadeEls.forEach(el => el.classList.add('fade-in'));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger siblings slightly
      const delay = (i % 4) * 80;
      setTimeout(() => entry.target.classList.add('visible'), delay);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

fadeEls.forEach(el => observer.observe(el));

// ─── Contact form (Formspree) ───
const form        = document.getElementById('contact-form');
const formSuccess = document.getElementById('form-success');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Basic validation
  const name    = form.name.value.trim();
  const email   = form.email.value.trim();
  const message = form.message.value.trim();

  if (!name || !email || !message) {
    [form.name, form.email, form.message].forEach(field => {
      if (!field.value.trim()) {
        field.style.borderColor = '#c0392b';
        field.addEventListener('input', () => field.style.borderColor = '', { once: true });
      }
    });
    return;
  }

  const btn = form.querySelector('button[type="submit"]');
  btn.textContent = 'Sending…';
  btn.disabled = true;

  try {
    const response = await fetch('https://formspree.io/f/mojkvpog', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    });

    if (response.ok) {
      form.classList.add('hidden');
      formSuccess.classList.remove('hidden');
    } else {
      const data = await response.json();
      const msg = data.errors ? data.errors.map(e => e.message).join(', ') : 'Something went wrong. Please try again.';
      btn.textContent = msg;
      btn.disabled = false;
    }
  } catch {
    btn.textContent = 'Network error — please try again.';
    btn.disabled = false;
  }
});
