#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """GithubOrgClient.org returns expected result and get_json."""

        # Setup the mock return value
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Instantiate client and call .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called exactly once with the right URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert .org returns the mocked payload
        self.assertEqual(result, expected_payload)
