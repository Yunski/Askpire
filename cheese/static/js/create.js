$(document).ready(function () {
    $("#create-form").submit(function(e) {
        e.preventDefault();
        var name = $("#name").val();
        var email = $("#email").val();
        var password = $("#password").val();
        var url = $(this).attr("action");

        if (!name || !email || !password) return;

        var checkUser = $.get('/api/user?email=' + email);
        checkUser.done(function(response) {
            r = JSON.parse(response);
            if (r.user_exists === 'true') {
                $(".alert").show();
                return;
            }
            var createUser = $.post(url, { name: name, email: email, password: password });
            createUser.done(function(response) {
                r = JSON.parse(response);
                if (r.success === 'true') {
                    document.location.href = "/dashboard";
                } else {
                    document.location.href = "/create";
                }
            });
        });
    });
});
