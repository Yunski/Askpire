$(window).on("load", function() {
    AOS.init();
});

$(".parallax").scroll(function() {
    if ($(".parallax").scrollTop() > 160) {
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
