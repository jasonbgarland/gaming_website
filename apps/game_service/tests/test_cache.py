"""
Unit tests for the InMemoryCache class used by the IGDB client.
Tests set/get, expiry, delete, and clear operations.

"""

# pylint: disable=duplicate-code
import unittest
import time
from src.igdb.cache import InMemoryCache


class TestInMemoryCache(unittest.TestCase):
    """Unit tests for the InMemoryCache class."""

    def setUp(self):
        """Set up a new cache instance before each test."""
        self.cache = InMemoryCache()

    def test_set_and_get(self):
        """Test that set() and get() work for a valid key before expiry."""
        self.cache.set("foo", "bar", ttl=5)
        self.assertEqual("bar", self.cache.get("foo"))

    def test_expiry(self):
        """Test that a key expires after its TTL."""
        self.cache.set("baz", 123, ttl=1)
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("baz"))

    def test_delete(self):
        """Test that delete() removes a key from the cache."""
        self.cache.set("key", "value", ttl=5)
        self.cache.delete("key")
        self.assertIsNone(self.cache.get("key"))

    def test_clear(self):
        """Test that clear() removes all keys from the cache."""
        self.cache.set("a", 1, ttl=5)
        self.cache.set("b", 2, ttl=5)
        self.cache.clear()
        self.assertIsNone(self.cache.get("a"))
        self.assertIsNone(self.cache.get("b"))


if __name__ == "__main__":
    unittest.main()
