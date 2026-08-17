document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('a.brand.has-logo-image').forEach(function(a){
    a.innerHTML = '<span class="bb-wordmark">bim<span>&</span>beam</span>';
  });

  // Mobile nav toggle (bb-menu-btn / bb-links, used on the new-brand pages)
  var menuBtn = document.querySelector('.bb-menu-btn');
  var links = document.querySelector('.bb-links');
  if (menuBtn && links) {
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.addEventListener('click', function(){
      var open = links.classList.toggle('bb-links-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.textContent = open ? '✕' : '☰';
    });
    links.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        links.classList.remove('bb-links-open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.textContent = '☰';
      });
    });
  }

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.entry-content > *, .kb-row-layout-wrap').forEach(function(el){
    el.classList.add('bb-fade');
  });

  if (prefersReducedMotion) {
    document.querySelectorAll('.bb-fade').forEach(function(el){ el.classList.add('bb-visible'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('bb-visible'); io.unobserve(e.target); }
      });
    }, {threshold:0.1});
    document.querySelectorAll('.bb-fade').forEach(function(el){ io.observe(el); });
  }
});

