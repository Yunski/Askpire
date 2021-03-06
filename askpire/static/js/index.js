$(document).ready(function () {
    $(window).on('load scroll', function () {
        var scrolled = $(this).scrollTop();
        $('#title').css({
            'transform': 'translate3d(0, ' + -(scrolled * 0.65) + 'px, 0)', // parallax (20% scroll rate)
            'opacity': 1 - scrolled / 400 // fade out at 400px from top
        });
        $('#hero-vid').css('transform', 'translate3d(0, ' + -(scrolled * 0.65) + 'px, 0)'); // parallax (25% scroll rate)
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

    $(".section-panel .card").mouseover(function() {
        $(".profile-img", this).css("width", "50%");
        $(".profile-img", this).css("height", "50%");
        $(".profile-stats", this).css("width", "50%");
        $(".profile-stats", this).css("height", "50%");
        $(".card-details", this).addClass("expand");
    });

    $(".section-panel .card").mouseleave(function() {
        $(".profile-img", this).css("width", "100%");
        $(".profile-img", this).css("height", "100%");
        $(".profile-stats", this).css("width", "0%");
        $(".profile-stats", this).css("height", "0%");
        $(".card-details", this).removeClass("expand");
    });


    var app = angular.module('content-switcher', []);

    $('#Button1').click(function(){
      $(this).addClass("active");
      $('#Button2').removeClass("active")
      $('#Button3').removeClass("active")
    });

    $('#Button2').click(function(){
      $(this).addClass("active");
      $('#Button1').removeClass("active")
      $('#Button3').removeClass("active")
    });

    $('#Button3').click(function(){
      $(this).addClass("active");
      $('#Button2').removeClass("active")
      $('#Button1').removeClass("active")
    });

    $(window).on('load', function () {
      $("#Button1").click();
    });
});
