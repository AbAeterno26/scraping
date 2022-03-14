# extract.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to extract a subset from a dataset
# GitHub link: https://github.com/AbAeterno26/scraping.git

import pandas as pd
import argparse

def main(output_file_name, input_file_name, top_n_movies):
    # Read csv file
    movies_df = pd.read_csv(input_file_name)

    # Sort movies by rating and select the top 5
    movies_df = movies_df.sort_values(["year", "rating"], ascending = [True, False], ignore_index=True).groupby("year").head(top_n_movies)

    # Save results to output file
    movies_df.to_csv(output_file_name, index=False)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-n", "--top_n_movies", type=int, default = 5, help="starting year (default: 5)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.input, args.top_n_movies)