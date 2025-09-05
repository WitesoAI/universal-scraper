#!/usr/bin/env python3
"""
Example usage of the Universal Scraper module
"""

import os
from universal_scraper import UniversalScraper, scrape

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    # Initialize scraper with custom model
    scraper = UniversalScraper(api_key=api_key, model_name="gemini-pro")
    
    # Set custom fields to extract
    scraper.set_fields([
        "company_name", 
        "job_title", 
        "apply_link", 
        "salary_range",
        "location",
        "job_description"
    ])
    
    print(f"Configured fields: {scraper.get_fields()}")
    print(f"Using model: {scraper.get_model_name()}")
    
    # Scrape a URL (replace with actual URL)
    try:
        url = "https://example-jobs-site.com"  # Replace with actual URL
        result = scraper.scrape_url(url, save_to_file=True)
        
        print(f"✅ Successfully scraped {url}")
        print(f"📊 Items extracted: {result['metadata']['items_extracted']}")
        print(f"💾 Saved to: {result.get('saved_to', 'Not saved')}")
        
        # Display sample data
        if result['data']:
            print("\n📋 Sample extracted data:")
            sample = result['data'][0] if isinstance(result['data'], list) else result['data']
            for field in scraper.get_fields():
                value = sample.get(field, "N/A")
                print(f"  {field}: {value}")
                
    except Exception as e:
        print(f"❌ Scraping failed: {e}")


def example_convenience_function():
    """Using the convenience function"""
    print("\n=== Convenience Function Example ===")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    try:
        # Quick scraping with convenience function and custom model
        result = scrape(
            url="https://example-jobs-site.com",  # Replace with actual URL
            api_key=api_key,
            fields=["company_name", "job_title", "apply_link"],
            model_name="gemini-1.5-pro"  # Custom model
        )
        
        print(f"✅ Quick scrape completed")
        print(f"📊 Items: {result['metadata']['items_extracted']}")
        
    except Exception as e:
        print(f"❌ Quick scraping failed: {e}")


def example_multiple_urls():
    """Scraping multiple URLs"""
    print("\n=== Multiple URLs Example ===")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    scraper = UniversalScraper(api_key=api_key)
    
    # Configure fields
    scraper.set_fields(["title", "link", "description", "price"])
    
    # List of URLs to scrape
    urls = [
        "https://example-site1.com",  # Replace with actual URLs
        "https://example-site2.com",
        "https://example-site3.com",
    ]
    
    try:
        results = scraper.scrape_multiple_urls(urls, save_to_files=True)
        
        successful = sum(1 for r in results if not r.get('error'))
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        for result in results:
            if result.get('error'):
                print(f"  Failed {result['url']}: {result['error']}")
            else:
                print(f"  Success {result['url']}: {result['metadata']['items_extracted']} items")
                
    except Exception as e:
        print(f"❌ Multiple URL scraping failed: {e}")


def example_custom_configuration():
    """Advanced configuration example"""
    print("\n=== Custom Configuration Example ===")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    # Initialize with custom directories and model
    scraper = UniversalScraper(
        api_key=api_key,
        temp_dir="custom_temp",
        output_dir="custom_output",
        log_level=10,  # DEBUG level
        model_name="gemini-1.5-pro"  # Custom model
    )
    
    # Set industry-specific fields
    scraper.set_fields([
        "product_name",
        "product_price", 
        "product_rating",
        "product_reviews_count",
        "product_availability",
        "product_description",
        "product_image_url"
    ])
    
    print(f"Custom fields configured: {scraper.get_fields()}")
    print(f"Using model: {scraper.get_model_name()}")
    
    try:
        # Scrape an e-commerce site
        url = "https://example-ecommerce.com"  # Replace with actual URL
        result = scraper.scrape_url(url, save_to_file=True)
        
        print(f"✅ E-commerce scraping completed")
        print(f"📁 Custom output directory used")
        
    except Exception as e:
        print(f"❌ Custom configuration scraping failed: {e}")


def example_model_switching():
    """Example showing how to switch models dynamically"""
    print("\n=== Model Switching Example ===")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    # Initialize with default model
    scraper = UniversalScraper(api_key=api_key)
    scraper.set_fields(["title", "description", "price"])
    
    print(f"Default model: {scraper.get_model_name()}")
    
    # Switch to a different model
    scraper.set_model_name("gemini-pro")
    print(f"Switched to model: {scraper.get_model_name()}")
    
    # Switch to another model
    scraper.set_model_name("gemini-1.5-pro")
    print(f"Switched to model: {scraper.get_model_name()}")
    
    print("✅ Model switching demonstrated")


if __name__ == "__main__":
    # Run all examples
    print("🚀 Universal Scraper Examples")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Please set GEMINI_API_KEY environment variable before running examples")
        print("   export GEMINI_API_KEY='your_api_key_here'")
        exit(1)
    
    # Run examples
    example_basic_usage()
    example_convenience_function()
    example_multiple_urls()
    example_custom_configuration()
    example_model_switching()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("\nNext steps:")
    print("1. Replace example URLs with real URLs you want to scrape")
    print("2. Customize the fields list for your specific use case")
    print("3. Check the output directory for extracted data files")