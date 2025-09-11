"""Basic tests for Universal Scraper"""


def test_import_main():
    """Test that main module can be imported"""
    import main

    assert main is not None


def test_import_universal_scraper():
    """Test that universal_scraper package can be imported"""
    import universal_scraper

    assert universal_scraper is not None


def test_basic_assertion():
    """Basic test to ensure pytest is working"""
    assert True
