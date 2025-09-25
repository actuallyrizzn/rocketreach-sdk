Security issue: API key leaked in repo; rotate and remove immediately

A RocketReach API key is committed in the repository.

Locations:
- docs/PROJECT_PLAN.md (API key printed inline)
- php/examples/basic_usage.php (hardcoded API key)

Actions:
- Revoke and rotate the API key in RocketReach
- Remove secrets from repo history (BFG Repo-Cleaner or git filter-repo)
- Replace examples/docs to use environment variables (e.g., ROCKETREACH_API_KEY)
- Add secret scanning (GitHub secret scanning, gitleaks) and pre-commit hooks

Acceptance criteria:
- Key rotated and removed from history
- Examples/docs updated to use env vars
- Secret scanning enabled
