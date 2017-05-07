$(document).ready(function () {
    $("#create-form").submit(function(e) {
        e.preventDefault();
        var name = $("#name").val();
        var email = $("#email").val();
        var password = $("#password").val();
        var url = $(this).attr("action");

        if (!name || !email || !password) return;

        var option = 0;
        if($('#option2').is(':checked')) {
            option = 1;
        }

        var createUser = $.post(url, { name: name, email: email, password: password, type: option });
        createUser.done(function(response) {
            r = JSON.parse(response);
            if (r.success === 'true') {
                document.location.href = "/dashboard";
            } else {
                $(".alert").show();
                return;
            }
        });
    });
});
