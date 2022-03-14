# scraper.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to scrape data from the web
# GitHub link: https://github.com/AbAeterno26/scraping.git
"""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse


def main(output_file_name, start_year, end_year):
    # Initialize movies dataframe
    movies_df = pd.DataFrame(columns=["title", "rating", "year", "stars", "runtime", "url"])
    
    # Extract movies from website until condition is met
    start = 1
    condition = False
    while not condition:
        # Load website with BeautifulSoup
        IMDB_URL = f'https://www.imdb.com/search/title/?title_type=feature&release_date={start_year}-01-01,{end_year}-01-01&num_votes=5000,&sort=user_rating,desc&start={start}&view=advanced'
        html = simple_get(IMDB_URL)
        dom = BeautifulSoup(html, 'lxml')

        # Extract movies from website
        temp_df = extract_movies(dom)
        movies_df = pd.concat([movies_df, temp_df])
        movies_df = movies_df.sort_values("year", ascending=True)
        
        # Update start to load next page
        start += 50
        
        # Check if at least 5 movies were released per year from start till end
        total_movies = movies_df.groupby(by=["year"]).size()
        if (total_movies >= 5).all() and end_year - start_year == len(total_movies):
            condition = True
        
    # Save results to output file
    movies_df.to_csv(output_file_name, index=False)

def extract_movies(dom):
    # Initialize dataframe for movies
    movies_df = []
    # Extract title, rating, year of release, stars, runtime, url from IMDB
    movies = dom.find_all("div", {"class": "lister-item-content"})
    movies_dict = {}
    for movie in movies:
        # Title
        title = movie.find("h3")
        movies_dict["title"] = title.a.text
        # Rating
        rating = movie.find("div", {"class":"inline-block ratings-imdb-rating"})
        movies_dict["rating"] = float(rating.strong.text)
        # Year of release
        year = movie.find("span", {"class":"lister-item-year text-muted unbold"})
        movies_dict["year"] = int(re.search(r'\d{4}', year.text)[0])
        # Stars
        try:
            stars = movie.find_all("p")[2]
            movies_dict["stars"] = stars.text.split("Stars:", 1)[1].replace('\n', '').replace(',', ';')
        except:
            movies_dict["stars"] = ""
        # Runtime
        runtime = movie.find("span", {"class":"runtime"})
        movies_dict["runtime"] = int(runtime.text.rsplit(" min")[0])
        # URL
        url = movie.find("h3", {"class":"lister-item-header"}).find('a')['href']
        movies_dict["url"] = "https://www.imdb.com/" + url
        # Append all information to dictionary
        movies_df.append(movies_dict)
    
    # Convert list with dictionaries to dataframe
    movies_df = pd.DataFrame(movies_df)
    return movies_df
    
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-s", "--start_year", type=int, default = 1930, help="starting year (default: 1930)")
    parser.add_argument("-e", "--end_year",   type=int, default = 2020, help="starting year (default: 2020)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.start_year, args.end_year)
