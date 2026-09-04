/* CornerHQ site behaviour. Four jobs, nothing else:
   1. Nav turns light once the hero has scrolled away (IntersectionObserver).
   2. Lightbox plays the full reel with sound.
   3. Enquiry form posts to Web3Forms and shows inline states.
   4. Reduced motion: no looping video, no smooth scroll. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Nav */
  var nav = document.getElementById('nav');
  var hero = document.getElementById('hero');
  if (nav && hero && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      nav.classList.toggle('is-light', !entries[0].isIntersecting);
    }, { rootMargin: '-72px 0px 0px 0px', threshold: 0 });
    io.observe(hero);
  }

  /* 2. Lightbox */
  var lightbox = document.getElementById('lightbox');
  var lightboxVideo = document.getElementById('lightbox-video');
  var lightboxClose = document.getElementById('lightbox-close');
  var FULL_REEL = 'video/reel-full.mp4';

  var lightboxOpener = null;

  function openLightbox(e) {
    if (!lightbox || !lightboxVideo) return;
    if (typeof lightbox.showModal !== 'function') {
      window.open(FULL_REEL, '_blank', 'noopener');
      return;
    }
    lightboxOpener = e && e.currentTarget ? e.currentTarget : null;
    if (!lightboxVideo.getAttribute('src')) lightboxVideo.setAttribute('src', FULL_REEL);
    lightbox.showModal();
    if (lightboxClose) lightboxClose.focus();
    lightboxVideo.currentTime = 0;
    var p = lightboxVideo.play();
    if (p && typeof p.catch === 'function') p.catch(function () {});
  }

  function closeLightbox() {
    if (lightbox && lightbox.open) lightbox.close();
  }

  Array.prototype.forEach.call(document.querySelectorAll('.btn-watch'), function (btn) {
    btn.addEventListener('click', openLightbox);
  });
  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target.classList.contains('lightbox-inner')) closeLightbox();
    });
    lightbox.addEventListener('close', function () {
      if (lightboxVideo) lightboxVideo.pause();
      if (lightboxOpener && typeof lightboxOpener.focus === 'function') lightboxOpener.focus();
      lightboxOpener = null;
    });
  }

  /* 3. Enquiry form */
  var form = document.getElementById('enquiry');
  var formError = document.getElementById('form-error');
  var formSuccess = document.getElementById('form-success');
  var formSubmit = document.getElementById('form-submit');

  function showError(msg) {
    if (formError) formError.textContent = msg;
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      showError('');

      var type = form.querySelector('input[name="Business type"]:checked');
      var name = form.querySelector('#f-name').value.trim();
      var business = form.querySelector('#f-business').value.trim();
      var email = form.querySelector('#f-email').value.trim();
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      if (!type) return showError('Tell us what you run.');
      if (!name) return showError('We need your name.');
      if (!business) return showError('We need the gym or promotion name.');
      if (!emailOk) return showError('That email does not look right.');

      formSubmit.disabled = true;
      formSubmit.textContent = 'Sending';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (!res.ok) throw new Error('bad status ' + res.status);
        form.hidden = true;
        formSuccess.classList.add('is-visible');
        formSuccess.focus();
      }).catch(function () {
        showError('That did not send. Give it a minute and try again.');
        formSubmit.disabled = false;
        formSubmit.textContent = 'Book a call';
      });
    });
  }

  /* 4. Reduced motion and media */
  var loops = document.querySelectorAll('.hero-video, .loop-video');
  if (reduceMotion) {
    Array.prototype.forEach.call(loops, function (v) {
      v.removeAttribute('autoplay');
      v.pause();
    });
  }

  /* Live site iframe: load after the page is idle, fade in when ready.
     If it never loads, the screenshot underneath stays visible. */
  var frame = document.querySelector('.site-frame');
  if (frame && frame.dataset.src) {
    var loadFrame = function () {
      frame.addEventListener('load', function () { frame.classList.add('is-loaded'); });
      frame.src = frame.dataset.src;
    };
    if ('requestIdleCallback' in window) requestIdleCallback(loadFrame, { timeout: 4000 });
    else setTimeout(loadFrame, 1500);
  }
})();
