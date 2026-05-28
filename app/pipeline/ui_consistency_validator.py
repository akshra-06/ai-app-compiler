
def normalize_route(route: str):

    return route.replace(
        "/{id}",
        ""
    )


def validate_ui_consistency(
    intent,
    api_schema,
    ui_schema
):

    errors = []

    valid_roles = set(
        intent.roles
    )

    # -----------------------------------
    # NORMALIZED API ROUTES
    # -----------------------------------

    api_routes = set()

    for endpoint in api_schema.endpoints:

        normalized = normalize_route(
            endpoint.path
        )

        api_routes.add(normalized)

    # -----------------------------------
    # PAGE VALIDATION
    # -----------------------------------

    for page in ui_schema.pages:

        normalized_page_route = (
            normalize_route(
                page.route
            )
        )

        # -------------------------
        # ROUTE VALIDATION
        # -------------------------

        if (
            normalized_page_route
            != "/login"
            and normalized_page_route
            not in api_routes
        ):

            errors.append(
                f"UI route has no API: "
                f"{page.route}"
            )

        # -------------------------
        # ROLE VALIDATION
        # -------------------------

        for role in page.roles:

            if role not in valid_roles:

                errors.append(
                    f"Invalid UI role: "
                    f"{role}"
                )

        # -------------------------
        # DASHBOARD VALIDATION
        # -------------------------

        if (
            "Dashboard" in page.name
            and "analytics dashboard"
            not in intent.features
        ):

            errors.append(
                "Dashboard exists without "
                "analytics feature"
            )

        # -------------------------
        # COMPONENT VALIDATION
        # -------------------------

        if len(page.components) == 0:

            errors.append(
                f"{page.name} "
                f"has no components"
            )

    return errors

