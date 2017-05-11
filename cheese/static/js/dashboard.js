$(document).ready(function () {
    $("#profile-update-form").submit(function(e) {
        e.preventDefault();
        console.log($(this).attr("action"));
        /*
        var name = $("#name").val();
        var skype = $("#skype").val();
        var email = $("#email").val();
        var password = $("#password").val();
        var url = $(this).attr("action");

        if (!name || !skype || !email || !password) return;

        var option = 0;
        if($('#option2').is(':checked')) {
            option = 1;
        }

        var createUser = $.post(url, { name: name, skype: skype, email: email, password: password, type: option });
        createUser.done(function(response) {
            r = JSON.parse(response);
            if (r.success === 'true') {
                document.location.href = "/dashboard";
            } else {
                $(".alert").show();
                return;
            }
        });*/
    });
});
