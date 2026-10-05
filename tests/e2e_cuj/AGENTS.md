# Dedicated-workspace CUJs

Each CUJ owns a separate workspace. Subclass `BaseCujTest` from `base.py` and set
`WORKSPACE_URL`. Setup provides `self.workspace`, a Databricks SDK client using
`UG_CUJ_SP_CLIENT_ID` and `UG_CUJ_SP_CLIENT_SECRET` with OAuth M2M authentication.
Local runs may instead use an explicitly supplied `DATABRICKS_BEARER`; partial SP credentials fail.
Do not share the workspace between concurrent runs. No stubbed configuration.

Run from the repository root with `scripts/run_integration.py --suite e2e-cuj` to install
ug and pinned agent versions and keep the parent suite's mocked fixtures out of CUJs.
Set `UG_CUJ_SP_CLIENT_ID` and `UG_CUJ_SP_CLIENT_SECRET`; local runs can instead supply
`DATABRICKS_BEARER`. CUJ1 also accepts `UG_CUJ1_WORKSPACE` to verify its assigned URL.
