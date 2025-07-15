#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class in the client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from unittest import TestCase


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
        """Test that has_license correctly checks for the license key."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        
        
class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide patching of get_json"""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the get_json patch"""
        cls.get_patcher.stop()