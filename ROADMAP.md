# Roadmap

This document outlines the planned features and improvements for Universal Scraper.

## Improve Reliability

- [ ] ⁠Retry Mechanism to re-generate the bs4 code till it is able to generate correct extraction code (beautifulsoup4 code)
- [ ] Captcha Resolve using Third Party api
- [ ] Decision making algo to switch to selenium for JS heavy sites for fetching HTML

## Extra Features

- [ ] Export data to excel (xslx) for adding formating & styling
    - [ ] Setting Appropriate Width of headers based on maxlenght of column's value
    - [ ] Setting Color (User should have ability to overwrite the default color)
- [ ] Add `min_limit` and `max_limit` parameters to `scrape_url()` method that replaces `DYNAMIC` placeholder with page numbers from min to max range, scrapes each URL sequentially, and aggregates results before saving.

```
e.g.

result = scraper.scrape_url("https://example.com/jobs?page=DYNAMIC", min_limit=1, max_limit=100)
```
- [ ] Giving Agent a functionality to scrap any website using this module: Add MCP (Model Context Protocal) in CLI to run a SSE (Server Side Event) API, which can be integrated in any Agent such as Claude Code, Cursor, etc