def setup_routes(app):
    container = app.container

    app.router.add_route(
        'POST', '/register', container.auth.register_user.as_view()
    )
    app.router.add_route(
        'POST', '/login', container.auth.authenticate_user.as_view()
    )
    app.router.add_route(
        'POST', '/logout', container.auth.logout_user.as_view()
    )
    app.router.add_route(
        'GET',  '/api/users/me', container.user.get_user_me.as_view()
    )
