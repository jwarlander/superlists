var initialize = function (navigator, user, token, urls) {
    $('#id_login').on('click', function () {
        navigator.id.request();
    });
    $('#id_logout').on('click', function () {
        navigator.id.logout();
    });

    navigator.id.watch({
        loggedInUser: user,
        onlogin: function (assertion) {
            $.post(
                urls.login,
                { assertion: assertion, csrfmiddlewaretoken: token }
            )
                .done(function () { window.location.reload(); })
                .fail(function () { navigator.id.logout(); });
        },
        onlogout: function () { },
        onready: function () {
            $('<div id="id_login_done"></div>').insertAfter("#id_logout");
            $('<div id="id_logout_done"></div>').insertAfter("#id_login");
        }
    })
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
