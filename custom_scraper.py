#!/usr/bin/env python3
"""
Custom scraper for AmbitionBox that waits for dynamic content to load
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def scrape_ambitionbox_companies():
    """Scrape AmbitionBox companies with custom waiting logic"""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = 'https://www.ambitionbox.com/companies-in-bengaluru'
        logger.info(f"Loading {url}")
        driver.get(url)
        
        # Wait for initial page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll down to trigger lazy loading
        logger.info("Scrolling to trigger content loading...")
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Wait for company content to appear (look for common patterns)
        logger.info("Waiting for company content...")
        time.sleep(10)  # Give more time for dynamic content
        
        html = driver.page_source
        logger.info(f"Page loaded with {len(html)} characters")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        companies = []
        
        # Strategy 1: Look for anchor tags that might be company links
        links = soup.find_all('a', href=True)
        company_links = []
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Filter for company-related links
            if ('/companies/' in href or 
                (text and len(text) > 3 and len(text) < 100 and 
                 any(keyword in text.lower() for keyword in ['tech', 'solutions', 'systems', 'services', 'ltd', 'limited', 'inc', 'corp']))):
                
                company_data = {
                    'name': text,
                    'url': href if href.startswith('http') else f"https://www.ambitionbox.com{href}",
                    'type': 'company_link'
                }
                company_links.append(company_data)
        
        logger.info(f"Found {len(company_links)} potential company links")
        
        # Strategy 2: Look for div elements that might contain company cards
        divs = soup.find_all('div')
        company_cards = []
        
        for div in divs:
            text = div.get_text(strip=True)
            # Look for divs that might be company cards
            if (text and len(text) > 10 and len(text) < 300 and
                any(keyword in text.lower() for keyword in ['rating', 'reviews', 'jobs', 'salary', 'interview'])):
                
                # Try to extract company name (usually the first significant text)
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                if lines:
                    company_name = lines[0]
                    if len(company_name) > 3 and len(company_name) < 100:
                        company_data = {
                            'name': company_name,
                            'description': text,
                            'type': 'company_card'
                        }
                        company_cards.append(company_data)
        
        logger.info(f"Found {len(company_cards)} potential company cards")
        
        # Strategy 3: Look for list items or other structured content
        list_items = soup.find_all(['li', 'article', 'section'])
        structured_companies = []
        
        for item in list_items:
            text = item.get_text(strip=True)
            if (text and len(text) > 5 and len(text) < 200 and
                not any(word in text.lower() for word in ['privacy', 'terms', 'cookie', 'login', 'signup'])):
                
                # Look for company-like patterns
                if any(pattern in text.lower() for pattern in ['technologies', 'solutions', 'systems', 'services', 'company']):
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    if lines:
                        company_name = lines[0]
                        structured_companies.append({
                            'name': company_name,
                            'content': text,
                            'type': 'structured_item'
                        })
        
        logger.info(f"Found {len(structured_companies)} structured company items")
        
        # Combine all results
        all_companies = company_links + company_cards + structured_companies
        
        # Remove duplicates based on name
        seen_names = set()
        unique_companies = []
        for company in all_companies:
            name = company['name'].lower().strip()
            if name not in seen_names and len(name) > 2:
                seen_names.add(name)
                unique_companies.append(company)
        
        logger.info(f"Final result: {len(unique_companies)} unique companies")
        
        return unique_companies
        
    except Exception as e:
        logger.error(f"Error scraping: {e}")
        return []
    
    finally:
        driver.quit()

if __name__ == "__main__":
    companies = scrape_ambitionbox_companies()
    
    # Save results
    result = {
        'url': 'https://www.ambitionbox.com/companies-in-bengaluru',
        'timestamp': time.time(),
        'total_companies': len(companies),
        'companies': companies
    }
    
    with open('ambitionbox_companies_custom.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Scraped {len(companies)} companies and saved to ambitionbox_companies_custom.json")
    
    # Show first few companies as preview
    for i, company in enumerate(companies[:10]):
        print(f"{i+1}. {company['name'][:50]} ({company['type']})")