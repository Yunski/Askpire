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

 // Additional, potentially unnecessary code
$(document).ready(function () {
    $(window).on('load scroll', function () {
        var scrolled = $(this).scrollTop();
        $('#title').css({
            'transform': 'translate3d(0, ' + -(scrolled * 0.2) + 'px, 0)', // parallax (20% scroll rate)
            'opacity': 1 - scrolled / 400 // fade out at 400px from top
        });
        $('#hero-vid').css('transform', 'translate3d(0, ' + -(scrolled * 0.25) + 'px, 0)'); // parallax (25% scroll rate)
    });

    // video controls
    $('#state').on('click', function () {
        var video = $('#hero-vid').get(0);
        var icons = $('#state > span');
        $('#overlay').toggleClass('fade');
        if (video.paused) {
            video.play();
            icons.removeClass('iconicfill-play').addClass('iconicfill-pause');
        } else {
            video.pause();
            icons.removeClass('iconicfill-pause').addClass('iconicfill-play');
        }
    });
});
