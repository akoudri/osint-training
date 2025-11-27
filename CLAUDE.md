# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OSINT (Open Source Intelligence) training repository focused on web scraping techniques. The project demonstrates three fundamental approaches to data collection:

1. **Static scraping** (static_scraping.py) - HTTP-based scraping using requests and BeautifulSoup
2. **Dynamic scraping** (dynamic_scraping.py) - Browser automation with Selenium for JavaScript-rendered content and authentication
3. **Social media extraction** (twitter_extractor.py) - Twitter/X data collection with advanced search queries (dorking)

## Architecture

### Static Scraping Pipeline (static_scraping.py)
Three-phase approach:
1. **Collection** - Uses requests with spoofed User-Agent headers for basic OPSEC
2. **Extraction** - BeautifulSoup parses HTML and extracts structured data (quotes, authors, tags)
3. **Storage** - Pandas DataFrame exports to CSV (utf-8-sig encoding for Excel compatibility)

Target: http://quotes.toscrape.com (public training site)

### Dynamic Scraping with Authentication (dynamic_scraping.py)
Browser automation workflow:
1. Firefox WebDriver initialization
2. Form interaction via Selenium (By.ID selectors)
3. Authentication verification (checks for "Logout" in page source)
4. Post-login data extraction
5. Proper cleanup with driver.quit()

Credentials (test site): `agent_osint` / `password123`

### Twitter/X Extraction with Dorking (twitter_extractor.py)
Advanced social media OSINT workflow:
1. Manual authentication (bypasses anti-bot protections and CAPTCHA)
2. Advanced search query injection with URL encoding (Twitter dorking syntax)
3. Progressive scrolling to load more tweets (configurable scroll count)
4. Set-based deduplication of extracted tweets
5. Graceful error handling with diagnostic messages

Key features:
- Supports complex Twitter search operators (`from:`, `to:`, `@`, `-filter:`, `OR`)
- Chronological sorting (`&f=live`)
- Headless mode support
- WebDriverWait for robust element detection
- Configurable via `REQUETE_BRUTE`, `HEADLESS`, `SCROLL_COUNT`

See TWITTER_EXTRACTOR_GUIDE.md for detailed usage and query syntax examples.

## Development Environment

### Setup
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- requests 2.32.5 - HTTP client
- beautifulsoup4 4.14.2 - HTML parsing
- pandas 2.3.3 - Data manipulation and CSV export
- selenium 4.38.0 - Browser automation

## Running Scripts

### Static Scraping
```bash
python static_scraping.py
```
Output: `resultats_quotes.csv` in project root

### Dynamic Scraping (requires Firefox)
```bash
python dynamic_scraping.py
```
Browser window opens automatically, performs login, then closes after 5 seconds

### Twitter/X Extraction (requires Firefox and Twitter account)
```bash
python twitter_extractor.py
```
Opens login page, waits for manual authentication, then executes search and scrolls to collect tweets. See TWITTER_EXTRACTOR_GUIDE.md for query syntax examples.

## Key Implementation Patterns

### BeautifulSoup Selectors
- Class-based: `soup.find_all('div', class_='quote')`
- Nested extraction: `bloc.find('span', class_='text').text`
- Multiple elements: `find_all('a', class_='tag')`

### Selenium Locators
- ID-based (preferred): `driver.find_element(By.ID, "username")`
- Class-based: `driver.find_element(By.CLASS_NAME, "text")`
- CSS selectors: `By.CSS_SELECTOR, 'article[data-testid="tweet"]'`
- Explicit waits: `WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))`

### Selenium Best Practices (Applied in corrected scripts)
- Use `Service(geckodriver_path)` for explicit driver path
- Use `WebDriverWait` instead of `time.sleep()` for dynamic content
- Add try/except with helpful error messages for initialization failures
- Always use `driver.quit()` in finally block
- Support headless mode via `Options().add_argument("--headless")`

### OPSEC Considerations
- User-Agent spoofing in HEADERS dict (static scraping)
- Progressive delays to avoid rate limiting
- Manual authentication for platforms with anti-bot protections
- Deduplication to avoid processing same data twice
- Proper error handling (status_code checks, try/except blocks)

## Common Issues

### Selenium Firefox Driver
If `webdriver.Firefox()` fails, ensure geckodriver is installed:
```bash
# Linux (Debian/Ubuntu)
sudo apt install firefox-geckodriver

# Mac
brew install geckodriver

# Or download from: https://github.com/mozilla/geckodriver/releases
```

### CSV Encoding
Uses `utf-8-sig` encoding to ensure proper display in Excel (includes BOM for Windows compatibility)
