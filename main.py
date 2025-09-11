#!/usr/bin/env python3
"""
Universal Web Scraper CLI
A command-line interface for AI-powered web scraping with
multi-provider support.

Usage:
    universal-scraper <URL> [--output OUTPUT_FILE] [--api-key API_KEY]
    [--model MODEL]

Example:
    universal-scraper https://example.com/jobs --output jobs_data.json
    universal-scraper https://example.com/products --api-key YOUR_KEY
    --model gpt-4
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from urllib.parse import urlparse

from universal_scraper.scraper import UniversalScraper


def setup_logging(level):
    """Setup logging configuration"""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def validate_url(url):
    """Validate URL format"""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        if parsed.scheme not in ["http", "https"]:
            return False
        return True
    except Exception:
        return False


def generate_output_filename(url, format_type="json"):
    """Generate output filename based on URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = "json" if format_type == "json" else "csv"
    return f"{domain}_{timestamp}.{extension}"


def scrape_multiple_urls(urls_file, scraper, output_dir, format_type="json"):
    """Scrape multiple URLs from a file"""
    if not os.path.exists(urls_file):
        print(f"❌ URLs file not found: {urls_file}")
        return False

    with open(urls_file, "r") as f:
        urls = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    if not urls:
        print(f"❌ No valid URLs found in {urls_file}")
        return False

    print(f"📋 Found {len(urls)} URLs to scrape")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    results = scraper.scrape_multiple_urls(
        urls, save_to_files=True, format=format_type
    )

    successful = sum(1 for r in results if not r.get("error"))
    failed = len(results) - successful

    print("\n📊 Batch scraping completed:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print("📁 Results saved to: output directory")

    if failed > 0:
        print("\n❌ Failed URLs:")
        for result in results:
            if result.get("error"):
                print(
                    f"  - {result['url']}: "
                    f"{result.get('error', 'Unknown error')}"
                )
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Universal Web Scraper - AI-powered structured data extraction "
            "with multi-provider support"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  universal-scraper https://example.com/jobs
  universal-scraper https://example.com/products --output products.json
  universal-scraper https://news.ycombinator.com --api-key YOUR_GEMINI_KEY
  universal-scraper https://example.com/data --api-key YOUR_OPENAI_KEY
  --model gpt-4
  universal-scraper https://example.com/content
  --api-key YOUR_ANTHROPIC_KEY --model claude-3-haiku-20240307
  universal-scraper --urls urls.txt --output-dir scraped_data --format csv

Multi-Provider Support:
  • Gemini (default): Set GEMINI_API_KEY or use --api-key with Gemini key
  • OpenAI: Use --api-key with OpenAI key and --model gpt-4/gpt-4o-mini/etc.
  • Anthropic: Use --api-key with Anthropic key and --model claude-3-*/etc.
  • 100+ others: See https://docs.litellm.ai/docs/providers
        """,
    )

    # URL input options
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument("url", nargs="?", help="URL to scrape")
    url_group.add_argument(
        "--urls", help="File containing URLs to scrape (one per line)"
    )

    # Output options
    parser.add_argument(
        "--output", "-o", help="Output filename for extracted data"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for final results (default: output)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)",
    )

    # AI Provider configuration
    parser.add_argument(
        "--api-key",
        help=(
            "AI provider API key (or set GEMINI_API_KEY/OPENAI_API_KEY/"
            "ANTHROPIC_API_KEY env var)"
        ),
    )
    parser.add_argument(
        "--model",
        help=(
            "AI model name (e.g., gemini-2.5-flash, gpt-4, "
            "claude-3-haiku-20240307)"
        ),
    )

    # Field configuration
    parser.add_argument(
        "--fields",
        nargs="+",
        help=(
            "Fields to extract (e.g., --fields product_name product_price "
            "product_rating)"
        ),
    )

    # Logging options
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Minimal output"
    )

    # Legacy support
    parser.add_argument(
        "--gemini-key", help="Gemini API key (deprecated, use --api-key)"
    )
    parser.add_argument(
        "--temp-dir",
        default="temp",
        help="Temporary directory (default: temp)",
    )
    parser.add_argument("--save-html", help="Save cleaned HTML to this file")

    args = parser.parse_args()

    # Set log level
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    setup_logging(log_level)

    try:
        # Determine API key (legacy support)
        api_key = args.api_key or args.gemini_key

        # Initialize scraper with multi-provider support
        scraper = UniversalScraper(
            api_key=api_key,
            temp_dir=args.temp_dir,
            output_dir=args.output_dir,
            log_level=log_level,
            model_name=args.model,
        )

        # Set custom fields if provided
        if args.fields:
            scraper.set_fields(args.fields)
            print(f"🎯 Custom fields set: {args.fields}")

        # Show current configuration
        print(f"🤖 Using AI model: {scraper.get_model_name()}")
        print(f"📋 Extraction fields: {scraper.get_fields()}")

        if args.url:
            # Single URL scraping
            if not validate_url(args.url):
                print(f"❌ Invalid URL format: {args.url}")
                sys.exit(1)

            # Generate filename if not provided
            output_filename = args.output or generate_output_filename(
                args.url, args.format
            )

            print(f"🌐 Scraping URL: {args.url}")
            print(f"📁 Output format: {args.format.upper()}")

            result = scraper.scrape_url(
                url=args.url,
                save_to_file=True,
                output_filename=output_filename,
                format=args.format,
            )

            if not result.get("error"):
                print("\n✅ Scraping completed successfully!")
                print(
                    f"📄 Data saved to: "
                    f"{result.get('saved_to', output_filename)}"
                )
                print(
                    f"📊 Items extracted: "
                    f"{result['metadata']['items_extracted']}"
                )
                size_reduction = (
                    len(result['metadata']) -
                    result['metadata']['cleaned_html_length']
                )
                print(f"🗜️ HTML size reduction: {size_reduction}")

                # Save cleaned HTML if requested
                if args.save_html:
                    # This would require modifying scraper to return
                    # cleaned HTML
                    print(
                        f"💾 Cleaned HTML would be saved to: "
                        f"{args.save_html}"
                    )

                sys.exit(0)
            else:
                print(
                    f"\n❌ Scraping failed: "
                    f"{result.get('error', 'Unknown error')}"
                )
                sys.exit(1)

        elif args.urls:
            # Multiple URLs scraping
            print("📋 Batch scraping mode")
            print(f"📁 Output directory: {args.output_dir}")
            print(f"📄 Output format: {args.format.upper()}")

            success = scrape_multiple_urls(
                args.urls, scraper, args.output_dir, args.format
            )

            if success:
                print("\n✅ Batch scraping completed successfully!")
                sys.exit(0)
            else:
                print("\n❌ Batch scraping completed with errors!")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
