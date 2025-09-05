#!/usr/bin/env python3
"""
Universal Web Scraper
A modular web scraping system that fetches HTML, cleans it, and extracts structured data using AI.

Usage:
    python main.py <URL> [--output OUTPUT_FILE] [--gemini-key GEMINI_API_KEY]

Example:
    python main.py https://example.com/jobs --output jobs_data.json
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from urllib.parse import urlparse

from html_fetcher import HtmlFetcher
from html_cleaner import HtmlCleaner
from data_extractor import DataExtractor

class UniversalScraper:
    def __init__(self, gemini_api_key=None, log_level=logging.INFO, temp_dir="temp", output_dir="output"):
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        
        # Create directories
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize modules with temp directories
        self.fetcher = HtmlFetcher(temp_dir=temp_dir)
        self.cleaner = HtmlCleaner(temp_dir=temp_dir)
        
        try:
            self.extractor = DataExtractor(api_key=gemini_api_key, temp_dir=temp_dir, output_dir=output_dir)
        except ValueError as e:
            self.logger.error(f"Failed to initialize DataExtractor: {e}")
            raise
    
    def setup_logging(self, level):
        """Setup logging configuration"""
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def validate_url(self, url):
        """Validate URL format"""
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            if parsed.scheme not in ['http', 'https']:
                return False
            return True
        except Exception:
            return False
    
    def generate_output_filename(self, url):
        """Generate output filename based on URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{domain}_{timestamp}.json"
    
    def scrape(self, url, output_file=None, clean_html_file=None, format='json'):
        """
        Main scraping method that orchestrates all three modules
        
        Args:
            url (str): URL to scrape
            output_file (str): Optional output filename for extracted data
            clean_html_file (str): Optional filename to save cleaned HTML
            format (str): Output format - 'json' (default) or 'csv'
            
        Returns:
            dict: Results of the scraping process
        """
        self.logger.info(f"Starting scraping process for: {url}")
        
        # Validate URL
        if not self.validate_url(url):
            error_msg = f"Invalid URL format: {url}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        try:
            # Step 1: Fetch HTML
            self.logger.info("=" * 50)
            self.logger.info("STEP 1: FETCHING HTML")
            self.logger.info("=" * 50)
            
            raw_html = self.fetcher.fetch_html(url)
            self.logger.info(f"Fetched HTML content: {len(raw_html)} characters")
            
            # Step 2: Clean HTML
            self.logger.info("=" * 50)
            self.logger.info("STEP 2: CLEANING HTML")
            self.logger.info("=" * 50)
            
            cleaned_html = self.cleaner.clean_html(raw_html, url=url)
            self.logger.info(f"Cleaned HTML content: {len(cleaned_html)} characters")
            
            # Optionally save cleaned HTML
            if clean_html_file:
                with open(clean_html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_html)
                self.logger.info(f"Cleaned HTML saved to: {clean_html_file}")
            
            # Step 3: Extract structured data
            self.logger.info("=" * 50)
            self.logger.info("STEP 3: EXTRACTING DATA WITH AI")
            self.logger.info("=" * 50)
            
            # Ensure output file goes to output directory if no path specified
            if output_file and not os.path.dirname(output_file):
                output_file = os.path.join(self.output_dir, output_file)
            
            extraction_result = self.extractor.extract_and_save(
                cleaned_html, 
                url=url, 
                output_file=output_file,
                format=format
            )
            
            if extraction_result['success']:
                self.logger.info("=" * 50)
                self.logger.info("SCRAPING COMPLETED SUCCESSFULLY!")
                self.logger.info("=" * 50)
                self.logger.info(f"📄 Data file: {extraction_result['data_file']}")
                self.logger.info(f"🐍 Code file: {extraction_result['code_file']}")
                self.logger.info(f"📊 Items extracted: {extraction_result['extracted_items']}")
                
                return {
                    "success": True,
                    "url": url,
                    "raw_html_length": len(raw_html),
                    "cleaned_html_length": len(cleaned_html),
                    "data_file": extraction_result['data_file'],
                    "code_file": extraction_result['code_file'],
                    "extracted_items": extraction_result['extracted_items']
                }
            else:
                error_msg = f"Data extraction failed: {extraction_result['error']}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Scraping failed: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def scrape_multiple(self, urls, output_dir="scraped_data", format='json'):
        """Scrape multiple URLs"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = []
        for i, url in enumerate(urls, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"PROCESSING URL {i}/{len(urls)}: {url}")
            self.logger.info(f"{'='*60}")
            
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"{domain}_{timestamp}.json")
            
            result = self.scrape(url, output_file, format=format)
            result['url'] = url
            results.append(result)
            
            if not result['success']:
                self.logger.error(f"Failed to scrape {url}: {result.get('error', 'Unknown error')}")
        
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Universal Web Scraper - AI-powered structured data extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://example.com/jobs
  python main.py https://example.com/products --output products.json
  python main.py https://news.ycombinator.com --gemini-key YOUR_API_KEY
  python main.py --urls urls.txt --output-dir scraped_data
        """
    )
    
    # URL input options
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument('url', nargs='?', help='URL to scrape')
    url_group.add_argument('--urls', help='File containing URLs to scrape (one per line)')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output filename for extracted data')
    parser.add_argument('--output-dir', default='output', 
                       help='Output directory for final results (default: output)')
    parser.add_argument('--temp-dir', default='temp',
                       help='Temporary directory for intermediate files (default: temp)')
    parser.add_argument('--save-html', help='Save cleaned HTML to this file')
    parser.add_argument('--format', '-f', choices=['json', 'csv'], default='json',
                       help='Output format (default: json)')
    
    # API configuration
    parser.add_argument('--gemini-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
    
    # Logging options
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal output')
    
    args = parser.parse_args()
    
    # Set log level
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    try:
        # Initialize scraper
        scraper = UniversalScraper(
            gemini_api_key=args.gemini_key,
            log_level=log_level,
            temp_dir=args.temp_dir,
            output_dir=args.output_dir
        )
        
        if args.url:
            # Single URL scraping
            result = scraper.scrape(
                url=args.url,
                output_file=args.output,
                clean_html_file=args.save_html,
                format=args.format
            )
            
            if result['success']:
                print(f"\n✅ Scraping completed successfully!")
                print(f"📄 Data saved to: {result['data_file']}")
                print(f"🐍 Extraction code saved to: {result['code_file']}")
                print(f"📊 Items extracted: {result['extracted_items']}")
                sys.exit(0)
            else:
                print(f"\n❌ Scraping failed: {result['error']}")
                sys.exit(1)
                
        elif args.urls:
            # Multiple URLs scraping
            if not os.path.exists(args.urls):
                print(f"❌ URLs file not found: {args.urls}")
                sys.exit(1)
            
            with open(args.urls, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                print(f"❌ No valid URLs found in {args.urls}")
                sys.exit(1)
            
            print(f"📋 Found {len(urls)} URLs to scrape")
            results = scraper.scrape_multiple(urls, args.output_dir, format=args.format)
            
            successful = sum(1 for r in results if r['success'])
            failed = len(results) - successful
            
            print(f"\n📊 Batch scraping completed:")
            print(f"✅ Successful: {successful}")
            print(f"❌ Failed: {failed}")
            print(f"📁 Results saved to: {args.output_dir}")
            
            if failed > 0:
                print("\n❌ Failed URLs:")
                for result in results:
                    if not result['success']:
                        print(f"  - {result['url']}: {result.get('error', 'Unknown error')}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()