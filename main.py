

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# Set Chrome options 

options = webdriver.ChromeOptions()


# Setup ChromeDriver automatically

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)


# Open IMDb Top 250 page

url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Wait for page to load

time.sleep(5)  #  gives time for JavaScript content to load

# Extract movie details

movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

movie_list = []

for movie in movies:
    title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
    rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
    
    movie_list.append({
        "Movie Name": title,
        "IMDb Rating": rating
    })


# Save data to CSV

df = pd.DataFrame(movie_list)
df.to_csv("imdb_top_250.csv", index=False)


# Close the browser

driver.quit()

print("IMDb Top 250 movies scraped successfully!")
