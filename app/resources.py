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
    app.router.add_route(
        'GET', '/api/exclusive-events', container.event.get_global_events.as_view()
    )
    app.router.add_route(
        'POST', '/api/events', container.event.create_event.as_view()
    )
    app.router.add_route(
        'POST', '/api/events/{event_id}/messages', container.chat.post_message.as_view()
    )
    app.router.add_route(
        'GET', '/api/events/{event_id}/messages', container.chat.get_messages.as_view()
    )
    app.router.add_route(
        'GET', '/api/events/{event_id}', container.event.get_event_by_id.as_view()
    )
    app.router.add_route(
        'POST', '/api/events/{event_id}/join', container.event.join_to_event.as_view()
    )
    app.router.add_route(
        'GET', '/api/my-events', container.event.get_my_events.as_view()
    )
    app.router.add_route(
        'GET', '/api/events', container.event.get_all_events.as_view()
    )
    app.router.add_route(
        'POST', '/api/events/{event_id}/feedback', container.event.create_feedback.as_view()
    )
    app.router.add_route(
        'POST', '/api/events/{eventId}/leave', container.event.leave_event.as_view()
    )
