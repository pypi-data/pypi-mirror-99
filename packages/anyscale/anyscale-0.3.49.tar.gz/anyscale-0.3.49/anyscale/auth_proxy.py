import urllib

from aiohttp import web
from aiohttp_middlewares import cors_middleware  # type: ignore

from anyscale import ANYSCALE_ENV


async def error_page(request: web.Request) -> web.Response:
    # Serve custom error page for the services
    return web.Response(
        text="""
<html>
    <head>
        <title> Retrying </title>
        <meta http-equiv="refresh" content="5">
        <style>
        body {
            font-family: noto sans,sans-serif;
            padding: 25px;
        }
        </style>
    </head>
    <body>
      <h1>
        Loading...
      </h1>

      <h2> ⌛ </h2>
      <p> Service currently unavailable. </p>
      <p> This page will automatically refresh. </p>

    </body>
</html>
        """,
        status=502,  # bad gateway
        content_type="text/html",
    )


async def index(request: web.Request) -> web.Response:
    token = request.query.get("token")
    redirect_to = request.query.get("redirect_to")
    # Sometimes we don't want to perform the redirect.
    # We just want to authenticate and download the cookie,
    # for example in the case of the WebTerminal.
    auth_only = request.query.get("auth_only")

    path = {
        "tensorboard": "/tensorboard/",
        "grafana": "/grafana/",
        "dashboard": "/",
        "hosted_dashboard": "/metrics/redirect",
        "webterminal": "/webterminal/",
        "anyscaled": "/anyscaled/",
        "metrics": "/metrics",
    }

    if not token or not redirect_to or redirect_to not in path.keys():
        return web.Response(
            text="token or redirect_to field not found, "
            "maybe you forgot to add `?token=..&redirect_to.` field? "
            "redirect_to={tensorboard, dashboard, grafana, webterminal}.",
            status=401,
        )

    resp = (
        web.HTTPFound(path[redirect_to])
        if auth_only is None
        else web.Response(text="ok")
    )
    use_secure = (
        ANYSCALE_ENV["ANYSCALE_HOST"] == "https://beta.anyscale.com"
        and redirect_to != "dashboard"
    )
    if redirect_to == "webterminal":
        # The default for samesite is None currently but it is migrating
        # to Lax for most browser. Explicitly setting it here will
        # enable beta.anyscale.com to communicate with webterminal service.
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
        resp.set_cookie("anyscale-token", token, secure=True, samesite="None")
    else:
        resp.set_cookie("anyscale-token", token, secure=use_secure)
    return resp


async def authorize(request: web.Request) -> web.Response:
    print(
        "Got authorizatoin request for:",
        request.headers.get("X-Forwarded-Uri", "unknown"),
    )
    cookies = request.cookies
    if cookies.get("anyscale-token") == request.config_dict["auth_token"]:
        return web.Response(text="Authorized", status=200)
    else:
        # Prometheus does not set a cookie
        if request.headers.get("X-Forwarded-Uri") == "/metrics":
            ref = request.headers.get("Referer", "")
            token_list = urllib.parse.parse_qs(urllib.parse.urlsplit(ref).query).get(
                "token", []
            )
            if (
                len(token_list) == 1
                and token_list[0] == request.config_dict["auth_token"]
            ):
                return web.Response(text="Authorized", status=200)
        return web.Response(text="Unauthorized", status=401)


def make_auth_proxy_app(auth_token: str) -> web.Application:
    auth_app = web.Application()
    auth_app.add_routes(
        [
            web.get("/", index),
            web.get("/authorize", authorize),
            web.get("/error_page", error_page),
        ]
    )

    origins = []
    # ANYSCALE_ENV is only a dictionary values when
    # this server runs on the head node.
    # If its a dictionary, use the ANYSCALE_HOST as whitelisted host
    # these values could be an IP address in developer instances
    # or beta.anyscale.com in production
    if "ANYSCALE_HOST" in ANYSCALE_ENV:
        origins = [ANYSCALE_ENV["ANYSCALE_HOST"]]

    app = web.Application(
        middlewares=[cors_middleware(origins=origins, allow_credentials=True)]
    )

    app.add_subapp("/auth", auth_app)
    app["auth_token"] = auth_token

    return app
