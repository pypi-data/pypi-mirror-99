from __future__ import annotations
from abc import abstractproperty, ABCMeta
from datetime import datetime, timedelta
from json import JSONDecodeError
import os
import typing as t
import warnings

from piccolo.apps.user.tables import BaseUser
from starlette.exceptions import HTTPException
from starlette.endpoints import HTTPEndpoint, Request
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    JSONResponse,
)
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates

from piccolo_api.session_auth.tables import SessionsBase


if t.TYPE_CHECKING:
    from starlette.responses import Response


TEMPLATES = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


class SessionLogoutEndpoint(HTTPEndpoint, metaclass=ABCMeta):
    @abstractproperty
    def _session_table(self) -> t.Type[SessionsBase]:
        raise NotImplementedError

    @abstractproperty
    def _cookie_name(self) -> str:
        raise NotImplementedError

    async def post(self, request: Request) -> PlainTextResponse:
        cookie = request.cookies.get(self._cookie_name, None)
        if not cookie:
            raise HTTPException(
                status_code=401, detail="The session cookie wasn't found."
            )
        await self._session_table.remove_session(token=cookie)

        response = PlainTextResponse("Successfully logged out")
        response.set_cookie(self._cookie_name, "", max_age=0)
        return response


class SessionLoginEndpoint(HTTPEndpoint, metaclass=ABCMeta):
    @abstractproperty
    def _auth_table(self) -> t.Type[BaseUser]:
        raise NotImplementedError

    @abstractproperty
    def _session_table(self) -> t.Type[SessionsBase]:
        raise NotImplementedError

    @abstractproperty
    def _session_expiry(self) -> timedelta:
        raise NotImplementedError

    @abstractproperty
    def _max_session_expiry(self) -> timedelta:
        raise NotImplementedError

    @abstractproperty
    def _cookie_name(self) -> str:
        raise NotImplementedError

    @abstractproperty
    def _redirect_to(self) -> t.Optional[str]:
        """
        Where to redirect to after login is successful. It's the name of a
        Starlette route.
        """
        raise NotImplementedError

    @abstractproperty
    def _production(self) -> bool:
        """
        If True, apply more stringent security.
        """
        raise NotImplementedError

    async def get(self, request: Request) -> HTMLResponse:
        template = TEMPLATES.get_template("login.html")

        # If CSRF middleware is present, we have to include a form field with
        # the CSRF token. It only works if CSRFMiddleware has
        # allow_form_param=True, otherwise it only looks for the token in the
        # header.
        csrftoken = request.scope.get("csrftoken")
        csrf_cookie_name = request.scope.get("csrf_cookie_name")

        return HTMLResponse(
            template.render(
                csrftoken=csrftoken, csrf_cookie_name=csrf_cookie_name
            )
        )

    async def post(self, request: Request) -> Response:
        # Some middleware (for example CSRF) has already awaited the request
        # body, and adds it to the request.
        body = request.scope.get("form")

        if not body:
            try:
                body = await request.json()
            except JSONDecodeError:
                body = await request.form()

        username = body.get("username", None)
        password = body.get("password", None)

        if (not username) or (not password):
            raise HTTPException(
                status_code=401, detail="Missing username or password"
            )

        user_id = await self._auth_table.login(
            username=username, password=password
        )

        if not user_id:
            raise HTTPException(status_code=401, detail="Login failed")

        now = datetime.now()
        expiry_date = now + self._session_expiry
        max_expiry_date = now + self._max_session_expiry

        session: SessionsBase = await self._session_table.create_session(
            user_id=user_id,
            expiry_date=expiry_date,
            max_expiry_date=max_expiry_date,
        )

        if self._redirect_to is not None:
            response: Response = RedirectResponse(
                url=self._redirect_to, status_code=HTTP_303_SEE_OTHER
            )
        else:
            response = JSONResponse(
                content={"message": "logged in"}, status_code=200
            )

        if not self._production:
            message = (
                "If running sessions in production, make sure 'production' "
                "is set to True, and serve under HTTPS."
            )
            warnings.warn(message)

        response.set_cookie(
            key=self._cookie_name,
            value=session.token,
            httponly=True,
            secure=self._production,
            max_age=int(self._max_session_expiry.total_seconds()),
            samesite="lax",
        )
        return response


def session_login(
    auth_table: t.Type[BaseUser] = BaseUser,
    session_table: t.Type[SessionsBase] = SessionsBase,
    session_expiry: timedelta = timedelta(hours=1),
    max_session_expiry: timedelta = timedelta(days=7),
    redirect_to: t.Optional[str] = "/",
    production: bool = False,
    cookie_name: str = "id",
) -> t.Type[SessionLoginEndpoint]:
    class _SessionLoginEndpoint(SessionLoginEndpoint):
        _auth_table = auth_table
        _session_table = session_table
        _session_expiry = session_expiry
        _max_session_expiry = max_session_expiry
        _redirect_to = redirect_to
        _production = production
        _cookie_name = cookie_name

    return _SessionLoginEndpoint


def session_logout(
    session_table: t.Type[SessionsBase] = SessionsBase,
    cookie_name: str = "id",
) -> t.Type[SessionLogoutEndpoint]:
    class _SessionLogoutEndpoint(SessionLogoutEndpoint):
        _session_table = session_table
        _cookie_name = cookie_name

    return _SessionLogoutEndpoint
