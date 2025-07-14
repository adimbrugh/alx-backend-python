#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google", {"login": "google", "id": 123}),
        ("abc", {"login": "abc", "id": 456}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns expected result and get_json is called correctly."""
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)
