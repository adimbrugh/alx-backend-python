

#!/usr/bin/env python3

from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map
from unittest import TestCase
from utils import get_json
from utils import memoize
import unittest




class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with parameterized inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))
        
        


class TestGetJson(TestCase):
    """Test get_json function with mocked HTTP GET requests."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected payload with mocked requests.get"""
        with patch("utils.requests.get") as mock_get:
            """Mock requests.get to return a predefined JSON payload."""
            # Mock the requests.get method
            # to simulate an HTTP GET request to test_url
            # and return a mock response with the test_payload
            # Patch the requests.get method
            # Create a mock response object with a .json method
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function
            # that uses requests.get to fetch JSON data
            # from the test_url
            # Call the get_json function with the test_url
            result = get_json(test_url)

            # Assert .get was called once with test_url
            # Assert that requests.get was called with the correct URL
            # Check that the mock_get was called with the test_url
            mock_get.assert_called_once_with(test_url)

            # Assert the function returns the mock payload
            # Check that the result matches the expected test_payload
            # Assert that the result is equal to the test_payload
            self.assertEqual(result, test_payload)




class TestMemoize(TestCase): 
    """Unit test for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result and calls the method only once."""

        class TestClass: 
            """A simple class to test the memoize decorator."""
            def a_method(self):
                return 42

            @memoize # Decorate a_method with memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            # Call a_property twice
            # to test that it is memoized
            # Call the memoized property a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Validate the return values
            # Check that both calls to a_property return the same value
            # and that the method was called only once
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Confirm a_method was called only once due to memoization
            mock_method.assert_called_once()
            # Check that the method was called only once
            # Assert that the mock_method was called exactly once
            
