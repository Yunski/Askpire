$(document).ready(function () {
    $("#profile-update-form").submit(function(e) {
        e.preventDefault();
        var firstName = $("#first-name").val();
        var lastName = $("#last-name").val();
        var skype = $("#skype").val();
        var school = $("#school").val();
        var major = $("#major").val();
        var year = $("#year").val();
        var satMath = $("#sat-math").val();
        var satReading = $("#sat-reading").val();
        var satWriting = $("#sat-writing").val();
        var act = $("#act").val();
        var description = $("#description").val();
        var url = $(this).attr("action");

        $.ajax({
            url: url,
            type: "PUT",
            data: { first_name: firstName,
                    last_name: lastName,
                    skype: skype,
                    school: school,
                    major: major,
                    year: year,
                    sat_math: satMath,
                    sat_reading: satReading,
                    sat_writing: satWriting,
                    act: act,
                    description: description },
            success: function(response) {
                r = JSON.parse(response);
                if (r.success === 'true') {
                    console.log("success");
                }
                document.location.href = "/profile";
            }
        });
    });
});
