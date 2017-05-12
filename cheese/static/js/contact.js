$(window).on("load", function() {
    AOS.init();
});


$(function(){
  $.stellar({
    horizontalScrolling: false,
    verticalOffset: 40
  });
});


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

 // Additional, potentially unnecessary code
$(document).ready(function () {
    $("#contact-form").submit(function(e) {
        e.preventDefault();
        document.location.href="/contact";
    });
});
