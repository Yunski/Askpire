$(document).ready(function () {
    var tabs = {"dashboard": 1, "profile": 2, "schedule": 3, "notifications": 4, "calendar": 3};
    var path = window.location.pathname.split("/")[1];
    $("#sidebar-nav li").removeClass("active");
    $("#sidebar-nav li:nth-child(" + tabs[path] + ")").addClass("active");
});
