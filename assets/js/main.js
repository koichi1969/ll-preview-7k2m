/* LOUVRELINE demo site - common script */
(function () {
  // mobile nav
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
    document.querySelectorAll('.gnav a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
    });
  }

  // active nav
  var path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.gnav a[data-page]').forEach(function (a) {
    var p = a.getAttribute('data-page');
    if (path === p || (p === 'cases.html' && location.pathname.indexOf('/cases/') !== -1)) a.classList.add('is-active');
  });

  // scroll reveal
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

  // case filter
  var filter = document.querySelector('.filter');
  if (filter) {
    filter.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      filter.querySelectorAll('button').forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
      var cat = btn.getAttribute('data-cat');
      document.querySelectorAll('.case-grid .case-card').forEach(function (c) {
        c.style.display = (cat === 'all' || c.getAttribute('data-cat') === cat) ? '' : 'none';
      });
    });
  }

  // lightbox
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    document.querySelectorAll('[data-zoom]').forEach(function (img) {
      img.addEventListener('click', function () {
        lbImg.src = img.getAttribute('data-zoom') || img.src;
        lb.classList.add('is-open');
      });
    });
    lb.addEventListener('click', function () { lb.classList.remove('is-open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.classList.remove('is-open'); });
  }

  // demo contact form
  var form = document.querySelector('.form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.style.display = 'none';
      var done = document.querySelector('.form-done');
      if (done) { done.style.display = 'block'; done.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    });
  }
})();
