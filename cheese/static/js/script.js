$(window).on("load", function() {
    AOS.init();
});


$(function(){

  $.stellar({
    horizontalScrolling: false,
    verticalOffset: 40
  });
});


$(".parallax").scroll(function() {
    if ($(".parallax").scrollTop() > 96) {
        $(".navbar-custom").addClass("shrink");
        //$(".navbar").addClass("fixed-top");
    } else {
        $(".navbar-custom").removeClass("shrink");
        $(".navbar-custom").css("-webkit-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("-moz-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("-o-transition", "height 300ms ease-in-out");
        $(".navbar-custom").css("transition", "height 300ms ease-in-out");
        //$(".navbar").removeClass("fixed-top");
    }
});
