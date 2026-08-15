document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('a.brand.has-logo-image').forEach(function(a){
    a.innerHTML = '<span class="bb-wordmark">bim<span>&</span>beam</span>';
  });

  document.querySelectorAll('.entry-content > *, .kb-row-layout-wrap').forEach(function(el){
    el.classList.add('bb-fade');
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('bb-visible'); io.unobserve(e.target); }
    });
  }, {threshold:0.1});
  document.querySelectorAll('.bb-fade').forEach(function(el){ io.observe(el); });
});
