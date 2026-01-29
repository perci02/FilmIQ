from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# Enable Headless Mode

options = webdriver.ChromeOptions()
options.add_argument("--headless")      
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# Setup ChromeDriver automatically

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)


# Open IMDb Top 250 page

driver.get("https://www.imdb.com/chart/top/")

time.sleep(10)

#  Check page title and print available selectors
print("Page title:", driver.title)
print("Page URL:", driver.current_url)

# Try different selectors to find movies
movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
print(f"Found {len(movies)} movies with first selector")

# If first selector doesn't work, try alternative selectors
if len(movies) == 0:
    movies = driver.find_elements(By.CSS_SELECTOR, "li[data-testid='chart-list-item']")
    print(f"Trying alternative selector: Found {len(movies)} movies")

if len(movies) == 0:
    movies = driver.find_elements(By.XPATH, "//li[contains(@class, 'ipc-metadata')]")
    print(f"Trying XPATH selector: Found {len(movies)} movies")

# Extract movie data

data = []

for movie in movies:
    try:
        # Extract title
        title_elem = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
        title = title_elem.text.split('\n')[0].strip()  
        
        # Extract rating 
        rating_elem = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
        rating = rating_elem.text.split('\n')[0].strip()  

        data.append({
            "Movie Name": title,
            "IMDb Rating": rating
        })
    except Exception as e:
        print(f"Error extracting movie data: {e}")
        continue


# Save to CSV

df = pd.DataFrame(data)
df.to_csv("imdb_top_250.csv", index=False)


# Close browser

driver.quit()
print("Scraping completed successfully in headless mode!")