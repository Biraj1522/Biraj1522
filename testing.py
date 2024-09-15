import pytest
import os
import json
from pathlib import Path
from bookmark import BookmarkManager  # Import your BookmarkManager class

BOOKMARKS_FILE = Path("bookmarks.json")  # Path to your JSON file

@pytest.fixture(autouse=True)
def clean_bookmarks_file():
    """Ensure bookmarks.json is clean before and after tests."""
    if BOOKMARKS_FILE.exists():
        BOOKMARKS_FILE.unlink()  # Delete if exists
    yield
    if BOOKMARKS_FILE.exists():
        BOOKMARKS_FILE.unlink()  # Cleanup after tests

def test_add_bookmark():
    manager = BookmarkManager()
    manager.add_bookmark("https://www.ato.gov.au/", ["Aus gov"])
    bookmarks = manager.list_bookmarks()
    assert len(bookmarks) == 1
    assert bookmarks[0]["url"] == "https://www.ato.gov.au/"
    assert bookmarks[0]["tags"] == ["Aus gov"]

def test_no_duplicate_bookmarks():
    manager = BookmarkManager()
    manager.add_bookmark("https://www.ato.gov.au/", ["Aus gov"])
    manager.add_bookmark("https://www.ato.gov.au/", ["Aus gov"])
    bookmarks = manager.list_bookmarks()
    assert len(bookmarks) == 1  # Only one entry, no duplicates

def test_empty_bookmarks_list():
    manager = BookmarkManager()
    bookmarks = manager.list_bookmarks()
    assert bookmarks == []  # Should return an empty list when no bookmarks

def test_persistence():
    manager = BookmarkManager()
    manager.add_bookmark("https://www.ato.gov.au/", ["Aus gov"])
    manager.save_bookmarks()

    # Load again to check persistence
    new_manager = BookmarkManager()
    bookmarks = new_manager.list_bookmarks()
    assert len(bookmarks) == 1
    assert bookmarks[0]["url"] == "https://www.ato.gov.au/"
