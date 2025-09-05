#!/usr/bin/env python3
"""
Test script for the Universal Scraper module
"""

import os
import sys
import tempfile
import json
from unittest.mock import Mock, patch

def test_import():
    """Test if the module can be imported"""
    print("🧪 Testing module import...")
    try:
        from universal_scraper import UniversalScraper, scrape
        print("✅ Module import successful")
        return True
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False

def test_initialization():
    """Test module initialization"""
    print("🧪 Testing initialization...")
    try:
        from universal_scraper import UniversalScraper
        
        # Test initialization with dummy API key
        scraper = UniversalScraper(api_key="test_key")
        print("✅ Basic initialization successful")
        
        # Test with custom directories
        with tempfile.TemporaryDirectory() as temp_dir:
            scraper = UniversalScraper(api_key="test_key", temp_dir=temp_dir, output_dir=temp_dir)
            print("✅ Custom directory initialization successful")
        
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_field_configuration():
    """Test field configuration functionality"""
    print("🧪 Testing field configuration...")
    try:
        from universal_scraper import UniversalScraper
        
        scraper = UniversalScraper(api_key="test_key")
        
        # Test default fields
        default_fields = scraper.get_fields()
        assert isinstance(default_fields, list), "get_fields should return a list"
        print(f"✅ Default fields: {default_fields}")
        
        # Test setting custom fields
        custom_fields = ["title", "price", "description"]
        scraper.set_fields(custom_fields)
        
        # Verify fields were set
        current_fields = scraper.get_fields()
        assert current_fields == custom_fields, "Fields not set correctly"
        print(f"✅ Custom fields set: {current_fields}")
        
        # Test invalid fields
        try:
            scraper.set_fields([])  # Empty list should raise error
            print("❌ Empty fields should raise error")
            return False
        except ValueError:
            print("✅ Empty fields correctly rejected")
        
        try:
            scraper.set_fields("not a list")  # Non-list should raise error
            print("❌ Non-list fields should raise error")
            return False
        except ValueError:
            print("✅ Non-list fields correctly rejected")
        
        return True
    except Exception as e:
        print(f"❌ Field configuration test failed: {e}")
        return False

def test_url_validation():
    """Test URL validation"""
    print("🧪 Testing URL validation...")
    try:
        from universal_scraper import UniversalScraper
        
        scraper = UniversalScraper(api_key="test_key")
        
        # Test valid URLs
        valid_urls = [
            "https://example.com",
            "http://test.org/page",
            "https://subdomain.example.com/path?query=1"
        ]
        
        for url in valid_urls:
            if scraper._validate_url(url):
                print(f"✅ Valid URL accepted: {url}")
            else:
                print(f"❌ Valid URL rejected: {url}")
                return False
        
        # Test invalid URLs
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Wrong protocol
            "https://",  # Missing domain
            "",  # Empty string
        ]
        
        for url in invalid_urls:
            if scraper._validate_url(url):
                print(f"❌ Invalid URL accepted: {url}")
                return False
            else:
                print(f"✅ Invalid URL rejected: {url}")
        
        return True
    except Exception as e:
        print(f"❌ URL validation test failed: {e}")
        return False

def test_filename_generation():
    """Test filename generation"""
    print("🧪 Testing filename generation...")
    try:
        from universal_scraper import UniversalScraper
        
        scraper = UniversalScraper(api_key="test_key")
        
        test_urls = [
            "https://example.com",
            "https://www.test.org/page",
            "https://subdomain.site.com/path?query=1"
        ]
        
        for url in test_urls:
            filename = scraper._generate_filename(url)
            assert filename.endswith('.json'), "Filename should end with .json"
            assert len(filename) > 0, "Filename should not be empty"
            print(f"✅ Generated filename for {url}: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ Filename generation test failed: {e}")
        return False

def test_convenience_function():
    """Test the convenience scrape function"""
    print("🧪 Testing convenience function...")
    try:
        from universal_scraper import scrape
        
        # Test function exists and is callable
        assert callable(scrape), "scrape function should be callable"
        print("✅ Convenience function is callable")
        
        return True
    except Exception as e:
        print(f"❌ Convenience function test failed: {e}")
        return False

def test_mock_scraping():
    """Test scraping with mocked dependencies"""
    print("🧪 Testing mock scraping...")
    try:
        from universal_scraper import UniversalScraper
        
        # Mock the dependencies to avoid actual network calls
        with patch('html_fetcher.HtmlFetcher') as mock_fetcher:
            with patch('html_cleaner.HtmlCleaner') as mock_cleaner:
                with patch('universal_scraper.CustomDataExtractor') as mock_extractor:
                    
                    # Setup mocks
                    mock_fetcher_instance = Mock()
                    mock_fetcher.return_value = mock_fetcher_instance
                    mock_fetcher_instance.fetch_html.return_value = "<html><body>Test</body></html>"
                    
                    mock_cleaner_instance = Mock()
                    mock_cleaner.return_value = mock_cleaner_instance
                    mock_cleaner_instance.clean_html.return_value = "Clean HTML content"
                    
                    mock_extractor_instance = Mock()
                    mock_extractor.return_value = mock_extractor_instance
                    mock_extractor_instance.extract_data.return_value = [
                        {"title": "Test Job", "company": "Test Company"}
                    ]
                    
                    # Create scraper and test
                    scraper = UniversalScraper(api_key="test_key")
                    scraper.set_fields(["title", "company"])
                    
                    # This should work without making actual network calls
                    with tempfile.TemporaryDirectory() as temp_dir:
                        scraper.output_dir = temp_dir
                        result = scraper.scrape_url("https://example.com")
                        
                        assert result["url"] == "https://example.com"
                        assert "data" in result
                        assert "metadata" in result
                        print("✅ Mock scraping successful")
        
        return True
    except Exception as e:
        print(f"❌ Mock scraping test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Universal Scraper Module Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_import),
        ("Initialization Test", test_initialization),
        ("Field Configuration Test", test_field_configuration),
        ("URL Validation Test", test_url_validation),
        ("Filename Generation Test", test_filename_generation),
        ("Convenience Function Test", test_convenience_function),
        ("Mock Scraping Test", test_mock_scraping),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Module is ready to use.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)