# Changelog

All notable changes to this project will be documented in this file.

## v1.7.0 - HTML Form Optimization Release
- 🔧 **NEW**: Select options limiting - automatically reduces select tags to maximum 2 options
- 🧹 **ENHANCEMENT**: Improved HTML cleaning with form element optimization
- 📦 **OPTIMIZATION**: Further reduces HTML size by removing excessive form options
- 🎯 **FEATURE**: Smart form simplification preserves essential functionality while reducing complexity
- ⚡ **PERFORMANCE**: Reduced token usage in AI processing through cleaner HTML forms

## v1.6.0 - Enhanced CLI with Full Multi-Provider Support Release
- 🚀 **NEW**: Complete CLI rewrite with LiteLLM multi-provider support
- 🔧 **NEW**: CLI now supports OpenAI, Anthropic, and 100+ other AI models  
- 📝 **NEW**: `--api-key` and `--model` CLI arguments for any provider
- 🎯 **NEW**: `--fields` CLI argument for custom field extraction
- 🔄 **ENHANCEMENT**: Dynamic help examples showing `universal-scraper` instead of `python main.py`
- 📋 **ENHANCEMENT**: Better CLI error handling and user feedback
- 🌍 **ENHANCEMENT**: Environment variable auto-detection in CLI
- 🛠️ **API**: Backward compatible - existing CLI usage still works
- ⚡ **PERFORMANCE**: CLI now uses same optimized pipeline as Python API

## v1.5.0 - Multi-Provider AI Support Release
- 🚀 **NEW**: LiteLLM integration for 100+ AI models support
- 🤖 **NEW**: Support for OpenAI GPT models (gpt-4, gpt-3.5-turbo, etc.)
- 🧠 **NEW**: Support for Anthropic Claude models (claude-3-opus, claude-3-sonnet, claude-3-haiku)
- 🔧 **NEW**: Automatic provider detection based on API key patterns
- 🔧 **NEW**: Environment variable auto-detection (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY)
- 📝 **FEATURE**: Flexible model switching with `set_model_name()` method
- 🔄 **ENHANCEMENT**: Backward compatibility maintained - Gemini remains default
- 📚 **DOCS**: Comprehensive multi-provider usage examples and setup guides
- ⚡ **API**: Updated all methods to work seamlessly with any supported AI provider

## v1.4.0 - CSV Export Support Release
- 📊 **NEW**: CSV export functionality with `format='csv'` parameter
- 📈 **NEW**: Support for both JSON (default) and CSV output formats
- 🔧 **NEW**: CLI `--format` flag for choosing output format
- 📋 **FEATURE**: Automatic field detection and consistent CSV structure
- 🔄 **FEATURE**: Universal data format compatibility (Excel, Google Sheets, pandas)
- 📝 **DOCS**: Comprehensive CSV export documentation with examples
- 🛠️ **API**: Updated all scraping methods to support format parameter
- ✨ **ENHANCEMENT**: JSON remains the default format for backward compatibility

## v1.2.0 - Smart Caching & HTML Optimization Release
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

## v1.1.0
- ✨ **NEW**: Gemini model selection functionality
- 🔧 Added `model_name` parameter to `UniversalScraper()` constructor
- 🔧 Added `get_model_name()` and `set_model_name()` methods
- 🔧 Enhanced convenience `scrape()` function with `model_name` parameter  
- 🔄 Updated default model to `gemini-2.5-flash`
- 📚 Updated documentation with model examples
- ✅ Fixed missing `cloudscraper` dependency

## v1.0.0
- Initial release
- AI-powered field extraction
- Customizable field configuration
- Multiple URL support
- Comprehensive test suite