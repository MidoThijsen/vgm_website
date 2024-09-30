from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from summarize_headlines import filter_headlines
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import chromedriver_autoinstaller
import time

app = Flask(__name__)

# Global variable to store the scraped and filtered headlines per website
filtered_headlines = []

# ChromeDriver setup
def setup_driver():
    chromedriver_autoinstaller.install()  # This installs the correct version of ChromeDriver automatically
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run browser in headless mode
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# List of websites and their CSS selectors
websites = [
    {"url": "https://propertynl.com/", "selector": "div.column.column_2_3 ul li h2 a"},
    {"url": "https://www.nu.nl/", "selector": "#main ul li a div.item-title span span"},
    {"url": "https://www.volkskrant.nl/", "selector": "#main-content article.wl-tile a header h3 span.teaser__title__value--long strong"},
    {"url": "https://nos.nl/", "selector": "#content ul li a div h2"},
    {"url": "https://vastgoedjournaal.nl/", "selector": "#articles a article div.article-grid-item-right div"},
]

# Function to extract titles from a website using the provided CSS selector
def extract_titles(news_url, css_selector):
    # Initialize WebDriver for Chrome
    driver = setup_driver()
    
    # Open the website
    print(f"Opening URL: {news_url}")
    driver.get(news_url)
    
    try:
        print(f"Waiting for elements to appear using selector: {css_selector}")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        
        # Use the provided CSS selector to find all elements
        title_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        titles_text = [title.text for title in title_elements if title.text.strip()]
        
        # Close the driver
        print("Closing the driver...")
        driver.quit()
        
        return titles_text
    
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

# Function to scrape and filter headlines
def scrape_and_filter_headlines():
    global filtered_headlines
    filtered_headlines = []  # Reset for each scrape

    # Scrape headlines from each website
    for site in websites:
        titles = extract_titles(site["url"], site["selector"])
        if titles:
            titles.append(site["url"])
            # Join headlines into a single string and filter relevant ones
            titles_content = "\n".join(titles)
            relevant_headlines = filter_headlines(titles_content).split("\n")
            
            # Store the relevant headlines along with the website URL
            filtered_headlines.append({"url": site["url"], "headlines": relevant_headlines})

# Schedule the scraping and filtering job every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_and_filter_headlines, trigger="interval", minutes=15)
scheduler.start()

# Shutdown the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def home():
    return render_template('index.html', filtered_headlines=filtered_headlines)

if __name__ == '__main__':
    # Initial scrape and filter when the app starts
    scrape_and_filter_headlines()
    app.run(debug=False)
