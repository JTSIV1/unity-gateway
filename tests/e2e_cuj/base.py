"""Base class for CUJs with a dedicated workspace."""

import os
from typing import ClassVar

import pytest
from databricks.sdk import WorkspaceClient


class BaseCujTest:
    WORKSPACE_URL: ClassVar[str] = ""
    workspace: WorkspaceClient

    @pytest.fixture(autouse=True)
    def setup_workspace(self):
        if not self.WORKSPACE_URL:
            pytest.fail("Set WORKSPACE_URL on your CUJ test class.", pytrace=False)

        client_id = os.environ.get("UG_CUJ_SP_CLIENT_ID", "")
        client_secret = os.environ.get("UG_CUJ_SP_CLIENT_SECRET", "")
        if bool(client_id) != bool(client_secret):
            pytest.fail("Set both UG_CUJ_SP_CLIENT_ID and UG_CUJ_SP_CLIENT_SECRET.", pytrace=False)
        if client_id:
            self.workspace = WorkspaceClient(
                host=self.WORKSPACE_URL,
                client_id=client_id,
                client_secret=client_secret,
                auth_type="oauth-m2m",
            )
        elif bearer := os.environ.get("DATABRICKS_BEARER", "").strip():
            self.workspace = WorkspaceClient(host=self.WORKSPACE_URL, token=bearer)
        else:
            pytest.fail(
                "Set UG_CUJ_SP_CLIENT_ID and UG_CUJ_SP_CLIENT_SECRET, "
                "or DATABRICKS_BEARER for a local run.",
                pytrace=False,
            )
