#!/usr/bin/env python3
"""
Example usage of Universal Scraper with caching functionality.

This script demonstrates how the caching system reuses previously generated
BeautifulSoup code for similar HTML structures, reducing API calls and
improving performance.
"""

import os
import time
from universal_scraper import UniversalScraper


def main():
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        exit(1)
    
    # Initialize scraper with caching enabled (default)
    scraper = UniversalScraper(api_key=api_key, log_level=20)  # DEBUG level
    
    # Set custom fields
    scraper.set_fields(["company_name", "job_title", "apply_link", "salary_range", "location"])
    
    print(f"Using model: {scraper.get_model_name()}")
    print(f"Extraction fields: {scraper.get_fields()}")
    print()
    
    # Example URLs (you can replace these with real URLs)
    test_urls = [
        "https://example-job-site.com/jobs/1",  # Replace with real URLs
        "https://example-job-site.com/jobs/2",  # Similar structure
        "https://example-job-site.com/jobs/3",  # Should hit cache
        "https://another-site.com/careers/1",   # Different structure
    ]
    
    print("=== Demonstrating Cache Functionality ===\n")
    
    # First, show initial cache stats
    cache_stats = scraper.get_cache_stats()
    print(f"Initial cache stats: {cache_stats}")
    print()
    
    # Scrape URLs and measure performance
    for i, url in enumerate(test_urls, 1):
        print(f"--- Scraping URL {i}: {url} ---")
        
        start_time = time.time()
        try:
            result = scraper.scrape_url(url)
            end_time = time.time()
            
            print(f"✓ Success: {result['metadata']['items_extracted']} items extracted")
            print(f"⏱ Time taken: {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}")
        
        print()
    
    # Show final cache stats
    print("=== Final Cache Statistics ===")
    final_stats = scraper.get_cache_stats()
    for key, value in final_stats.items():
        print(f"{key}: {value}")
    print()
    
    # Demonstrate cache management
    print("=== Cache Management ===")
    
    # Show top cached URLs
    if final_stats.get('top_urls'):
        print("Top cached URLs:")
        for url_info in final_stats['top_urls']:
            print(f"  - {url_info['url']}: {url_info['uses']} uses")
        print()
    
    # Clean up old cache entries (demo)
    print("Cleaning up cache entries older than 30 days...")
    removed = scraper.cleanup_old_cache(30)
    print(f"Removed {removed} old entries")
    print()
    
    # Demonstrate disabling/enabling cache
    print("=== Cache Control ===")
    scraper.disable_cache()
    print("Cache disabled - next scrape will not use cache")
    
    scraper.enable_cache()
    print("Cache enabled - caching resumed")
    print()
    
    # Optional: Clear entire cache
    # print("Clearing entire cache...")
    # scraper.clear_cache()
    # print("Cache cleared")


def demo_cache_hit():
    """
    Demonstrate cache hit by scraping the same URL twice with identical structure.
    """
    print("=== Cache Hit Demonstration ===")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set, skipping demo")
        return
    
    scraper = UniversalScraper(api_key=api_key)
    scraper.set_fields(["title", "description", "price"])
    
    # Same URL - should demonstrate cache hit on second call
    test_url = "https://example.com/products"
    
    print("First scrape (will generate new code):")
    start_time = time.time()
    try:
        result1 = scraper.scrape_url(test_url)
        time1 = time.time() - start_time
        print(f"✓ First scrape completed in {time1:.2f} seconds")
    except Exception as e:
        print(f"✗ First scrape failed: {e}")
        return
    
    print("\nSecond scrape (should use cached code):")
    start_time = time.time()
    try:
        result2 = scraper.scrape_url(test_url)
        time2 = time.time() - start_time
        print(f"✓ Second scrape completed in {time2:.2f} seconds")
        
        if time2 < time1 * 0.5:  # Assume cache hit if significantly faster
            print("🚀 Cache hit detected - much faster execution!")
        else:
            print("ℹ No significant speedup detected (might be cache miss)")
            
    except Exception as e:
        print(f"✗ Second scrape failed: {e}")
    
    # Show cache stats
    stats = scraper.get_cache_stats()
    print(f"\nCache stats: {stats}")


if __name__ == "__main__":
    print("Universal Scraper - Cache Functionality Demo")
    print("=" * 50)
    print()
    
    # Check if we have API key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠ Warning: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key to run this demo:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        print()
        print("The demo will show cache functionality concepts but won't make real API calls.")
        print()
    
    try:
        main()
        print("\n" + "=" * 50)
        demo_cache_hit()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
    
    print("\nDemo completed!")