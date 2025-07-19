#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class in the client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
import fixtures
import requests


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload."""
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """public_repos_url returns correct value from mocked org."""
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test_org/repos"
            }

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(
                result, "https://api.github.com/orgs/test_org/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repo names"""
        mock_repos_payload = [
            {"id": 1, "name": "repo1"},
            {"id": 2, "name": "repo2"},
            {"id": 3, "name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fake.api/repos"

            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://fake.api/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """has_license correctly checks for the license key"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected_names,
        "apache2_repos": apache_repos,
    }
    for org, repos, expected_names, apache_repos in fixtures.TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration for GithubOrgClient.public_repos using fixtures"""

    @classmethod
    def setUpClass(cls):
        """patching requests.get and simulate GitHub API behavior"""
        cls.get_patcher = patch('requests.get')

        # Start patching requests.get
        cls.mock_get = cls.get_patcher.start()

        # Configure mock behavior using side_effect
        def side_effect(url):
            if url == f"https://api.github.com/orgs/google":
                response = unittest.mock.Mock()
                response.json.return_value = cls.org_payload
                return response
            elif url == cls.org_payload["repos_url"]:
                response = unittest.mock.Mock()
                response.json.return_value = cls.repos_payload
                return response
            raise ValueError(f"Unhandled URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected repo names list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license='apache-2.0' filter."""
        client = GithubOrgClient("google")
        filtered = client.public_repos(license="apache-2.0")
        self.assertEqual(filtered, self.apache2_repos)
