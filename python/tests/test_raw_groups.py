import asyncio

from keycloak_client.raw.groups import GroupRoutes, ROUTE_SPECS


class FakeResponse:
    def __init__(self, *, status_code: int = 200, payload: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload or {"ok": True}
        self.content = b"{}" if self._payload is not None else b""

    def json(self):
        return self._payload


class FakeTransport:
    def __init__(self) -> None:
        self.calls = []

    async def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return FakeResponse()


def test_groups_routes_call_transport() -> None:
    async def run() -> None:
        transport = FakeTransport()
        routes = GroupRoutes(transport)
        for method_name, http_method, route_path, params, auth_required in ROUTE_SPECS:
            fn = getattr(routes, method_name)
            kwargs = {p: "x" for p in params}
            result = await fn(**kwargs)
            assert result["ok"] is True
            call_method, call_path, call_kwargs = transport.calls[-1]
            assert call_method == http_method
            assert "{" not in call_path and "}" not in call_path
            assert call_kwargs.get("auth_required") == auth_required

    asyncio.run(run())
