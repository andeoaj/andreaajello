/* ─────────────────────────────────────────────
   main.js — Andrea Ajello Economist Website
───────────────────────────────────────────── */

// ─── Year in footer ───
document.querySelectorAll('.year').forEach(el => {
  el.textContent = new Date().getFullYear();
});

// ─── Navbar: add 'scrolled' class on scroll ───
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 30);
}, { passive: true });

// ─── Mobile hamburger ───
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.setAttribute('aria-expanded', isOpen);
});

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// ─── Collapsible abstracts ───
document.querySelectorAll('.abstract-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const entry  = btn.closest('.paper-entry');
    const body   = entry.querySelector('.abstract-body');
    const isOpen = body.classList.toggle('open');

    btn.textContent  = isOpen ? 'Abstract ↑' : 'Abstract ↓';
    btn.classList.toggle('open', isOpen);
    btn.setAttribute('aria-expanded', isOpen);
  });
});
