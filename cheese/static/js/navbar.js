$(window).scroll(function() {
    if ($(document).scrollTop() > $(".parallax-image").height()) {
        $(".navbar-custom").addClass("shrink");
        //$(".navbar").addClass("fixed-top");
    } else {
        $(".navbar-custom").removeClass("shrink");
        $(".navbar-custom").css("-webkit-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("-moz-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("-o-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("transition", "height 300ms ease-in-out");
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
