from utils import get_json

class GithubOrgClient:
    """GitHub API client."""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch organization metadata."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
