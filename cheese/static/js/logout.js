$(document).ready(function () {
    $("#logout").click(function(e) {
        e.preventDefault();
        var logout = $.post('/logout');
        logout.done(function(response) {
            r = JSON.parse(response);
            if (r.success === 'true') {
                document.location.href = "/";
            }
        });
    });
});
