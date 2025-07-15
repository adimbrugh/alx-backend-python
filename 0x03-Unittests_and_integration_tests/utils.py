#!/usr/bin/env python3
"""Utility functions for unit testing."""
import requests


def access_nested_map(nested_map, path):
    """Access value in a nested map by path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """GET JSON data from a URL."""
    return requests.get(url).json()


def memoize(method):
    """Memoization decorator."""
    attr_name = "_{}".format(method.__name__)

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
