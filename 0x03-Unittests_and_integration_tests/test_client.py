#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient



class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected result and get_json is called correctly."""

        # Setup the mock return value
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Instantiate client and call .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called exactly once with the right URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert .org returns the mocked payload
        self.assertEqual(result, expected_payload)


    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos URL from mocked org"""

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")


    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct repo names"""

        # Simulated JSON response from GitHub API
        mock_repos_payload = [
            {"id": 1, "name": "repo1"},
            {"id": 2, "name": "repo2"},
            {"id": 3, "name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        # Patch the _public_repos_url property to return a fake URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://fake.api/repos"

            # Initialize client and call public_repos
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()  # Ensure _public_repos_url was accessed
            mock_get_json.assert_called_once_with("https://fake.api/repos")