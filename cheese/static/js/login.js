$(document).ready(function () {
    $("#login-form").submit(function(e) {
        e.preventDefault();
        var email = $("#email").val();
        var password = $("#password").val();
        var url = $(this).attr("action");

        if (!email || !password) return;

        var posting = $.post(url, { email: email, password: password });
        posting.done(function(response) {
            r = JSON.parse(response);
            if (r.success === 'false') {
                $('.error-message').show();
                return;
            }
            document.location.href = '/dashboard';
        });
    });
});
