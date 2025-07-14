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
    
    @property
    def _public_repos_url(self):
        """Return the repos URL from the organization metadata."""
        return self.org["repos_url"]
    
    def public_repos(self):
        """Return list of public repo names."""
        url = self._public_repos_url
        repos = get_json(url)
        return [repo["name"] for repo in repos]