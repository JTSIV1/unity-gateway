"""Authentication boundaries for dedicated CUJ workspaces."""

import pytest

from tests.e2e_cuj import base
from tests.e2e_cuj.base import BaseCujTest


class _Cuj(BaseCujTest):
    WORKSPACE_URL = "https://example.cloud.databricks.com"


def test_local_run_uses_explicit_bearer(monkeypatch):
    monkeypatch.delenv("UG_CUJ_SP_CLIENT_ID", raising=False)
    monkeypatch.delenv("UG_CUJ_SP_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("DATABRICKS_BEARER", "local-test-token")
    created = []
    monkeypatch.setattr(base, "WorkspaceClient", lambda **kwargs: created.append(kwargs))

    BaseCujTest.setup_workspace.__wrapped__(_Cuj())

    assert created == [{"host": _Cuj.WORKSPACE_URL, "token": "local-test-token"}]


def test_partial_service_principal_credentials_fail_even_with_local_bearer(monkeypatch):
    monkeypatch.setenv("UG_CUJ_SP_CLIENT_ID", "incomplete-client-id")
    monkeypatch.delenv("UG_CUJ_SP_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("DATABRICKS_BEARER", "local-test-token")

    with pytest.raises(pytest.fail.Exception, match="Set both UG_CUJ_SP_CLIENT_ID"):
        BaseCujTest.setup_workspace.__wrapped__(_Cuj())
