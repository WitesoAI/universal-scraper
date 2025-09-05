<h1 align="center"> Universal Scraper</h1>

<h2 align="center"> The Python package for scraping data from any website</h2>

<p align="center">
<a href="https://pypi.org/project/universal-scraper/"><img alt="pypi" src="https://img.shields.io/pypi/v/universal-scraper.svg"></a>
<a href="https://pepy.tech/project/universal-scraper?versions=1*&versions=2*&versions=3*"><img alt="Downloads" src="https://pepy.tech/badge/universal-scraper"></a>
<a href="https://pepy.tech/project/universal-scraper?versions=1*&versions=2*&versions=3*"><img alt="Downloads" src="https://pepy.tech/badge/universal-scraper/month"></a>
<a href="https://github.com/WitesoAI/universal-scraper/commits/main"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/WitesoAI/universal-scraper?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/universal-scraper?style=flat-square"></a>
</p>

--------------------------------------------------------------------------

A Python module for AI-powered web scraping with customizable field extraction using Google's Gemini AI.

## Features

- 🤖 **AI-Powered Extraction**: Uses Google Gemini to intelligently extract structured data
- 🎯 **Customizable Fields**: Define exactly which fields you want to extract (e.g., company name, job title, salary)
- 🚀 **Smart Caching**: Automatically caches extraction code based on HTML structure - saves 90%+ API tokens on repeat scraping
- 🧹 **Smart HTML Cleaner**: Removes noise and reduces HTML by 91%+ - significantly cuts token usage for AI processing
- 🔧 **Easy to Use**: Simple API for both quick scraping and advanced use cases
- 📦 **Modular Design**: Built with clean, modular components
- 🛡️ **Robust**: Handles edge cases, missing data, and various HTML structures
- 💾 **Multiple Output Formats**: Support for both JSON (default) and CSV export formats
- 📊 **Structured Output**: Clean, structured data output with comprehensive metadata

## Installation (Recommended)

```
pip install universal-scraper
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Universal_Scrapper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install google-generativeai beautifulsoup4 requests selenium lxml html5lib fake-useragent
   ```

3. **Install the module**:
   ```bash
   pip install -e .
   ```

## Quick Start

### 1. Set up your API key

Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and set it as an environment variable:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 2. Basic Usage

```python
from universal_scraper import UniversalScraper

# Initialize the scraper (uses default model: gemini-2.5-flash)
scraper = UniversalScraper(api_key="your_gemini_api_key")

# Or initialize with a custom model
scraper = UniversalScraper(api_key="your_gemini_api_key", model_name="gemini-pro")

# Set the fields you want to extract
scraper.set_fields([
    "company_name", 
    "job_title", 
    "apply_link", 
    "salary_range",
    "location"
])

# Check current model
print(f"Using model: {scraper.get_model_name()}")

# Scrape a URL (default JSON format)
result = scraper.scrape_url("https://example.com/jobs", save_to_file=True)

print(f"Extracted {result['metadata']['items_extracted']} items")
print(f"Data saved to: {result.get('saved_to')}")

# Scrape and save as CSV
result = scraper.scrape_url("https://example.com/jobs", save_to_file=True, format='csv')
print(f"CSV data saved to: {result.get('saved_to')}")
```

### 3. Convenience Function

For quick one-off scraping:

```python
from universal_scraper import scrape

# Quick scraping with default JSON format
data = scrape(
    url="https://example.com/jobs",
    api_key="your_gemini_api_key",
    fields=["company_name", "job_title", "apply_link"]
)

# Quick scraping with CSV format
data = scrape(
    url="https://example.com/jobs",
    api_key="your_gemini_api_key",
    fields=["company_name", "job_title", "apply_link"],
    format="csv"
)

# Quick scraping with custom model
data = scrape(
    url="https://example.com/jobs",
    api_key="your_gemini_api_key",
    fields=["company_name", "job_title", "apply_link"],
    model_name="gemini-1.5-pro"
)

print(data['data'])  # The extracted data
```

## 📁 Export Formats

Universal Scraper supports multiple output formats to suit your data processing needs:

### JSON Export (Default)
```python
# JSON is the default format
result = scraper.scrape_url("https://example.com/jobs", save_to_file=True)
# or explicitly specify
result = scraper.scrape_url("https://example.com/jobs", save_to_file=True, format='json')
```

**JSON Output Structure:**
```json
{
  "url": "https://example.com",
  "timestamp": "2025-01-01T12:00:00",
  "fields": ["company_name", "job_title", "apply_link"],
  "data": [
    {
      "company_name": "Example Corp",
      "job_title": "Software Engineer", 
      "apply_link": "https://example.com/apply/123"
    }
  ],
  "metadata": {
    "raw_html_length": 50000,
    "cleaned_html_length": 15000,
    "items_extracted": 1
  }
}
```

### CSV Export
```python
# Export as CSV for spreadsheet analysis
result = scraper.scrape_url("https://example.com/jobs", save_to_file=True, format='csv')
```

**CSV Output:**
- Clean tabular format with headers
- All fields as columns, missing values filled with empty strings
- Perfect for Excel, Google Sheets, or pandas processing
- Automatically handles varying field structures across items

**Benefits of CSV:**
- 📊 **Spreadsheet Ready**: Import directly into Excel/Google Sheets
- 📈 **Data Analysis**: Perfect for pandas DataFrame processing
- 🔄 **Universal Format**: Compatible with virtually all data tools
- 📋 **Clean Structure**: Consistent column structure across all rows

### Multiple URLs with Format Choice
```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

# Save all as JSON (default)
results = scraper.scrape_multiple_urls(urls, save_to_files=True)

# Save all as CSV
results = scraper.scrape_multiple_urls(urls, save_to_files=True, format='csv')
```

### CLI Usage
```bash
# Default JSON output
python main.py https://example.com/jobs --output jobs.json

# CSV output
python main.py https://example.com/jobs --output jobs.csv --format csv

# Multiple URLs as CSV
python main.py --urls urls.txt --output-dir results --format csv
```

## 🧹 Smart HTML Cleaning

**Reduces HTML size by 91%+** before sending to AI - dramatically cuts token usage:

### What Gets Removed
- **Scripts & Styles**: JavaScript, CSS, and style blocks
- **Ads & Analytics**: Advertisement content and tracking scripts
- **Navigation**: Headers, footers, sidebars, and menu elements  
- **Metadata**: Meta tags, SEO tags, and hidden elements
- **Empty Elements**: Recursively removes empty div elements that don't contain meaningful content
- **Noise**: Comments, unnecessary attributes, and whitespace

### Repeating Structure Reduction (NEW!)
The cleaner now intelligently detects and reduces repeated HTML structures:

- **Pattern Detection**: Uses structural hashing + similarity algorithms to find repeated elements
- **Smart Sampling**: Keeps 2 samples from groups of 3+ similar structures (e.g., 20 job cards → 2 samples)
- **Structure Preservation**: Maintains document flow and parent-child relationships
- **AI Optimization**: Provides enough samples for pattern recognition without overwhelming the AI

### Empty Element Removal (NEW!)
The cleaner now intelligently removes empty div elements:

- **Recursive Processing**: Starts from innermost divs and works outward
- **Content Detection**: Preserves divs with text, images, inputs, or interactive elements
- **Structure Preservation**: Maintains parent-child relationships and avoids breaking important structural elements
- **Smart Analysis**: Removes placeholder/skeleton divs while keeping functional containers

**Example**: Removes empty animation placeholders like `<div class="animate-pulse"></div>` while preserving divs containing actual content.

### HTML Separation for Execution (NEW!)
The system uses a two-phase approach for optimal results:

- **Phase 1**: Cleaned HTML (91% smaller) sent to AI for BeautifulSoup code generation
- **Phase 2**: Original HTML used for code execution to extract ALL data items
- **Result**: Best of both worlds - efficient AI analysis + complete data extraction

### Benefits
- **Massive Token Reduction**: 91%+ smaller HTML means 91%+ fewer tokens to process
- **Complete Data Extraction**: AI gets clean structure, execution gets all data (no data loss)
- **Better AI Focus**: Clean HTML helps AI generate more accurate extraction code
- **Faster Processing**: Less data to analyze means faster response times
- **Cost Savings**: Fewer tokens = lower API costs per extraction
- **Intelligent Deduplication**: Removes repetitive structures while preserving unique content

### Real-World Example
```bash
# Example from job scraping site (URL redacted)
2025-09-05 21:11:41 - html_cleaner - INFO - Starting HTML cleaning process...
2025-09-05 21:11:41 - html_cleaner - INFO - Removed noise. Length: 102329
2025-09-05 21:11:41 - html_cleaner - INFO - Removed headers/footers. Length: 85144
2025-09-05 21:11:41 - html_cleaner - INFO - Focused on main content. Length: 85019
2025-09-05 21:11:41 - html_cleaner - INFO - Found 20 similar structures, keeping 2, removing 18
2025-09-05 21:11:41 - html_cleaner - INFO - Removed 10 repeating structure elements
2025-09-05 21:11:41 - html_cleaner - INFO - Removed repeating structures. Length: 42710
2025-09-05 21:11:41 - html_cleaner - INFO - Removed 341 empty div elements in 1 iterations
2025-09-05 21:11:41 - html_cleaner - INFO - Removed empty divs. Length: 21319
2025-09-05 21:11:41 - html_cleaner - INFO - HTML cleaning completed. Original: 257758, Final: 21319
2025-09-05 21:11:41 - html_cleaner - INFO - Reduction: 91.7%
2025-09-05 21:11:41 - data_extractor - INFO - Using HTML separation: cleaned for code generation, original for execution
2025-09-05 21:11:41 - data_extractor - INFO - Successfully extracted data with 10 items
```

**Results**: 258KB → 21KB (91.7% reduction) for AI analysis, but all 10 job items extracted from original HTML!

## 🚀 Smart Caching (NEW!)

**Saves 90%+ API tokens** by reusing extraction code for similar HTML structures:

### Key Benefits
- **Token Savings**: Avoids regenerating BeautifulSoup code for similar pages
- **Performance**: 5-10x faster scraping on cached structures  
- **Cost Reduction**: Significant API cost savings for repeated scraping
- **Automatic**: Works transparently - no code changes needed

### How It Works
- **Structural Hashing**: Creates hash based on HTML structure (not content)
- **Smart Matching**: Reuses code when URL domain + structure + fields match
- **Local SQLite DB**: Stores cached extraction codes permanently

### Cache Management
```python
scraper = UniversalScraper(api_key="your_key")

# View cache statistics
stats = scraper.get_cache_stats()
print(f"Cached entries: {stats['total_entries']}")
print(f"Total cache hits: {stats['total_uses']}")

# Clear old entries (30+ days)
removed = scraper.cleanup_old_cache(30)
print(f"Removed {removed} old entries")

# Clear entire cache
scraper.clear_cache()

# Disable/enable caching
scraper.disable_cache()  # For testing
scraper.enable_cache()   # Re-enable
```

## Advanced Usage

### Multiple URLs

```python
scraper = UniversalScraper(api_key="your_api_key")
scraper.set_fields(["title", "price", "description"])

urls = [
    "https://site1.com/products",
    "https://site2.com/items", 
    "https://site3.com/listings"
]

# Scrape all URLs and save as JSON (default)
results = scraper.scrape_multiple_urls(urls, save_to_files=True)

# Scrape all URLs and save as CSV for analysis
results = scraper.scrape_multiple_urls(urls, save_to_files=True, format='csv')

for result in results:
    if result.get('error'):
        print(f"Failed {result['url']}: {result['error']}")
    else:
        print(f"Success {result['url']}: {result['metadata']['items_extracted']} items")
```

### Custom Configuration

```python
scraper = UniversalScraper(
    api_key="your_api_key",
    temp_dir="custom_temp",      # Custom temporary directory
    output_dir="custom_output",  # Custom output directory  
    log_level=logging.DEBUG,     # Enable debug logging
    model_name="gemini-pro"      # Custom Gemini model
)

# Configure for e-commerce scraping
scraper.set_fields([
    "product_name",
    "product_price", 
    "product_rating",
    "product_reviews_count",
    "product_availability",
    "product_description"
])

# Check and change model dynamically
print(f"Current model: {scraper.get_model_name()}")
scraper.set_model_name("gemini-1.5-pro")
print(f"Switched to: {scraper.get_model_name()}")

result = scraper.scrape_url("https://ecommerce-site.com", save_to_file=True)
```

## API Reference

### UniversalScraper Class

#### Constructor
```python
UniversalScraper(api_key=None, temp_dir="temp", output_dir="output", log_level=logging.INFO, model_name=None)
```

- `api_key`: Gemini API key (optional if GEMINI_API_KEY env var is set)
- `temp_dir`: Directory for temporary files
- `output_dir`: Directory for output files
- `log_level`: Logging level
- `model_name`: Gemini model name (default: 'gemini-2.5-flash')

#### Methods

- `set_fields(fields: List[str])`: Set the fields to extract
- `get_fields() -> List[str]`: Get current fields configuration
- `get_model_name() -> str`: Get current Gemini model name
- `set_model_name(model_name: str)`: Change the Gemini model
- `scrape_url(url: str, save_to_file=False, output_filename=None, format='json') -> Dict`: Scrape a single URL
- `scrape_multiple_urls(urls: List[str], save_to_files=True, format='json') -> List[Dict]`: Scrape multiple URLs

### Convenience Function

```python
scrape(url: str, api_key: str, fields: List[str], model_name: Optional[str] = None, format: str = 'json') -> Dict
```

Quick scraping function for simple use cases.

## Output Format

The scraped data is returned in a structured format:

```json
{
  "url": "https://example.com",
  "timestamp": "2025-01-01T12:00:00",
  "fields": ["company_name", "job_title", "apply_link"],
  "data": [
    {
      "company_name": "Example Corp",
      "job_title": "Software Engineer", 
      "apply_link": "https://example.com/apply/123"
    }
  ],
  "metadata": {
    "raw_html_length": 50000,
    "cleaned_html_length": 15000,
    "items_extracted": 1
  }
}
```

## Common Field Examples

### Job Listings
```python
scraper.set_fields([
    "company_name",
    "job_title", 
    "apply_link",
    "salary_range",
    "location",
    "job_description",
    "employment_type",
    "experience_level"
])
```

### E-commerce Products
```python
scraper.set_fields([
    "product_name",
    "product_price",
    "product_rating", 
    "product_reviews_count",
    "product_availability",
    "product_image_url",
    "product_description"
])
```

### News Articles
```python
scraper.set_fields([
    "article_title",
    "article_content",
    "article_author",
    "publish_date", 
    "article_url",
    "article_category"
])
```

## Testing

Run the test suite to verify everything works:

```bash
python test_module.py
```

## Example Files

- `example_usage.py`: Comprehensive examples of different usage patterns
- `test_module.py`: Test suite for the module

## How It Works

1. **HTML Fetching**: Uses cloudscraper to fetch HTML content, handling anti-bot measures
2. **Smart HTML Cleaning**: Removes 91%+ of noise (scripts, ads, navigation, repeated structures, empty divs) while preserving data structure
3. **Structure-Based Caching**: Creates structural hash and checks cache for existing extraction code
4. **AI Code Generation**: Uses Google Gemini to generate custom BeautifulSoup code on cleaned HTML (only when not cached)
5. **Code Execution**: Runs the cached/generated code on original HTML to extract ALL data items
6. **JSON Output**: Returns complete, structured data with metadata and performance stats

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is valid and set correctly
2. **Empty Results**: The AI might need more specific field names or the page might not contain the expected data
3. **Network Errors**: Some sites block scrapers - the tool uses cloudscraper to handle most cases

### Debug Mode

Enable debug logging to see what's happening:

```python
import logging
scraper = UniversalScraper(api_key="your_key", log_level=logging.DEBUG)
```

## Core Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<table>
<tr>

<td align="center">
    <a href="https://github.com/PushpenderIndia">
        <kbd><img src="https://avatars3.githubusercontent.com/PushpenderIndia?size=400" width="100px;" alt=""/></kbd><br />
        <sub><b>Pushpender Singh</b></sub>
    </a><br />
    <a href="https://github.com/WitesoAI/universal-scraper/commits?author=PushpenderIndia" title="Code"> :computer: </a> 
</td>

<td align="center">
    <a href="https://github.com/Ayushi0405">
        <kbd><img src="https://avatars3.githubusercontent.com/Ayushi0405?size=400" width="100px;" alt=""/></kbd><br />
        <sub><b>Ayushi Gupta</b></sub>
    </a><br />
    <a href="https://github.com/WitesoAI/universal-scraper/commits?author=Ayushi0405" title="Code"> :computer: </a> 
</td>

</tr>
</tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

Contributions of any kind welcome!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_module.py`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### v1.4.0 - CSV Export Support Release
- 📊 **NEW**: CSV export functionality with `format='csv'` parameter
- 📈 **NEW**: Support for both JSON (default) and CSV output formats
- 🔧 **NEW**: CLI `--format` flag for choosing output format
- 📋 **FEATURE**: Automatic field detection and consistent CSV structure
- 🔄 **FEATURE**: Universal data format compatibility (Excel, Google Sheets, pandas)
- 📝 **DOCS**: Comprehensive CSV export documentation with examples
- 🛠️ **API**: Updated all scraping methods to support format parameter
- ✨ **ENHANCEMENT**: JSON remains the default format for backward compatibility

### v1.2.0 - Smart Caching & HTML Optimization Release
- 🚀 **NEW**: Intelligent code caching system - **saves 90%+ API tokens**
- 🧹 **HIGHLIGHT**: Smart HTML cleaner reduces payload by 91%+ - **massive token savings**
- 🔧 **NEW**: Structural HTML hashing for cache key generation
- 🔧 **NEW**: SQLite-based cache storage with metadata
- 🔧 **NEW**: Cache management methods: `get_cache_stats()`, `clear_cache()`, `cleanup_old_cache()`
- 🔧 **NEW**: Automatic cache hit/miss detection and logging  
- 🔧 **NEW**: URL normalization (removes query params) for better cache matching
- ⚡ **PERF**: 5-10x faster scraping on cached HTML structures
- 💰 **COST**: Significant API cost reduction (HTML cleaning + caching combined)
- 📁 **ORG**: Moved sample code to `sample_code/` directory

### v1.1.0
- ✨ **NEW**: Gemini model selection functionality
- 🔧 Added `model_name` parameter to `UniversalScraper()` constructor
- 🔧 Added `get_model_name()` and `set_model_name()` methods
- 🔧 Enhanced convenience `scrape()` function with `model_name` parameter  
- 🔄 Updated default model to `gemini-2.5-flash`
- 📚 Updated documentation with model examples
- ✅ Fixed missing `cloudscraper` dependency

### v1.0.0
- Initial release
- AI-powered field extraction
- Customizable field configuration
- Multiple URL support
- Comprehensive test suite
