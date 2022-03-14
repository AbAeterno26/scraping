# crawler.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to scrape webdata and write to a csv file
# GitHub link: https://github.com/AbAeterno26/scraping.git

from helpers import simple_get
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # Read csv file
    movies_df = pd.read_csv(input_file_name)
    
    # Initialize languages list
    languages_list = []
    
    # Load website with BeautifulSoup and add languages to list
    for url in movies_df["url"]:
        IMDB_URL = url
        html = simple_get(IMDB_URL)
        dom = BeautifulSoup(html, 'lxml')
        languages_list.append(extract_language(dom))
        
    # Extract language from BeautifulSoup object and add to movies
    movies_df["languages"] = pd.Series(languages_list)
        
    # Sort by year (ascending)
    movies_df = movies_df.sort_values("year", ascending=True)
    
    # Save results to output file
    movies_df.to_csv(output_file_name, index=False)
    
def extract_language(dom):  
    # Initialize list for languages
    lang_list = []
    
    # Extract language(s) from IMDB and append the language(s) to the list
    languages = dom.select("a[href*=language]")
    for language in languages:
        if language.get_text() != "None":
            lang_list.append(language.get_text())
            
    # Change comma to semicolon as separator
    lang_string = ";".join(lang_list)
    
    # Return the languages
    return lang_string

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("output", help = "output file (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)