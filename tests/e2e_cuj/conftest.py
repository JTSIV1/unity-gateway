"""Fixtures for dedicated-workspace CUJs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_INTEGRATION = Path(__file__).parents[1] / "integration"
_ROOT = _INTEGRATION.parents[1]
_SUITE = Path(__file__).parent
for _path in (_ROOT, _INTEGRATION, _SUITE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from base import BaseCujTest  # noqa: E402

from tests.integration.conftest import installed_binary as installed_binary  # noqa: E402,F401
from tests.integration.conftest import session as _integration_session  # noqa: E402

session = _integration_session


@pytest.fixture
def live_session(request, session):
    test = request.instance
    if not isinstance(test, BaseCujTest):
        pytest.fail("live_session requires a BaseCujTest instance.", pytrace=False)

    authorization = test.workspace.config.authenticate().get("Authorization", "")
    bearer = authorization.removeprefix("Bearer ").strip()
    if not bearer:
        pytest.fail("Workspace authentication returned no bearer token.", pytrace=False)
    session.env["DATABRICKS_BEARER"] = bearer
    return session
