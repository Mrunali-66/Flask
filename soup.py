import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL for Steam search results
url = "https://store.steampowered.com/search/?filter=topsellers"
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all game entries
games = soup.find_all("a", class_="search_result_row")

titles, release_dates, prices, ratings = [], [], [], []

for game in games:
    title = game.find("span", class_="title").text.strip() if game.find("span", class_="title") else "N/A"
    release_date = game.find("div", class_="search_released").text.strip() if game.find("div", class_="search_released") else "N/A"
    price = game.find("div", class_="discount_final_price").text.strip() if game.find("div", class_="discount_final_price") else "N/A"
    rating_tag = game.find("span", class_="search_review_summary")
    rating = rating_tag["data-tooltip-html"].split("<br>")[0] if rating_tag and rating_tag.has_attr("data-tooltip-html") else "N/A"

    titles.append(title)
    release_dates.append(release_date)
    prices.append(price)
    ratings.append(rating)

# Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Release Date": release_dates,
    "Price": prices,
    "Rating": ratings
})

# Save as CSV
df.to_csv("steam_games.csv", index=False, encoding="utf-8")
print("✅ Steam games data saved successfully to 'steam_games.csv'")
