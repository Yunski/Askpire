$(window).scroll(function() {
    if ($(document).scrollTop() > 10) {
        $(".navbar-custom").addClass("scroll");
    } else {
        $(".navbar-custom").removeClass("scroll");
        $(".navbar-custom").css("-webkit-transition", "all 300ms ease-in-out");
        $(".navbar-custom").css("-moz-transition", "all 300ms ease-in-out");
        $(".navbar-custom").css("-o-transition", "all 300ms ease-in-out");
        $(".navbar-custom").css("transition", "all 300ms ease-in-out");
    }
});

$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});
