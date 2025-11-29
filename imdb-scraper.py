import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/chart/top/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select("li.ipc-metadata-list-summary-item")

data = []

for rank, movie in enumerate(movies[:50], start=1):  # Top 50 only
    # Title & year
    title_tag = movie.select_one("h3")
    year_tag = movie.select_one("span.ipc-title__meta-year")
    rating_tag = movie.select_one("span.ipc-rating-star--rating")
    link_tag = movie.select_one("a.ipc-lockup-overlay")

    title = title_tag.get_text(strip=True) if title_tag else "N/A"
    year = year_tag.get_text(strip=True).strip("()") if year_tag else "N/A"
    rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
    movie_url = "https://www.imdb.com" + link_tag["href"] if link_tag else "N/A"

    # Visit individual movie page (to extract director/stars)
    movie_resp = requests.get(movie_url, headers=headers)
    movie_soup = BeautifulSoup(movie_resp.text, "html.parser")

    credits = movie_soup.select("a.ipc-metadata-list-item__list-content-item")
    people = [c.get_text(strip=True) for c in credits[:3]]  # first few credits
    directors_stars = ", ".join(people) if people else "N/A"

    data.append([rank, title, year, rating, movie_url, directors_stars])

# Save to CSV
df = pd.DataFrame(data, columns=["Rank", "Title", "Year", "Rating", "URL", "Directors/Stars"])
df.to_csv("imdb_top_50.csv", index=False, encoding="utf-8")

print("✅ Scraping complete! Saved imdb_top_50.csv")
