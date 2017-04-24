$(".menu-button").on("click", function() {
    $("nav").removeClass("show-filter");
    $("header div.options").toggleClass("show-menu");
});

$(".filter-button").on("click", function() {
    $("header div.options").removeClass("show-menu");
    $("nav").toggleClass("show-filter");
});

$("main").on("click", function() {
    $("header div.options").removeClass("show-menu");
    $("nav").removeClass("show-filter");
});

$("header h1").on("click", function() {
    $("header div.options").removeClass("show-menu");
    $("nav").removeClass("show-filter");
});

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var data = {
        name: profile.getName(),
        email: profile.getEmail(),
        img: profile.getImageUrl(),
        token: googleUser.getAuthResponse().id_token
    };
    return $.ajax({
        type: "POST",
        url: "/gconnect",
        contentTye: "application/octet-stream; charset=utf-8",
        data: data,
        success: function(res) {
            if(res) {
                console.log("Go home");
                window.location = "http://localhost:5000";
            } else {
                console.log("Stay here");
                window.location.reload();
            }
        }
    });
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        console.log("User sign out.");
    });
}
