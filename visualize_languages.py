# visualize_languages.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to create a plot
# GitHub link: https://github.com/AbAeterno26/scraping.git

import matplotlib.pyplot as plt
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # Read csv file
    movies_df = pd.read_csv(input_file_name)
        
    # Split the column languages at the semicolon to get each individual language
    movies_df["languages"] = movies_df["languages"].str.split(";")
    
    # Explode the languages column to transform the list into separate rows for each language
    movies_df = movies_df.explode("languages")
    
    # Create list with top 10 languages
    lang_top10 = movies_df["languages"].value_counts().head(10).index.values
    
    # Find the count for the languages per year
    lang_df = movies_df.groupby(["languages", "year"], as_index=False)[["year", "languages"]]
    lang_df = lang_df.value_counts("languages")

    # Filter out the top 10 languages from the dataframe
    lang_df = lang_df.loc[lang_df["languages"].isin(lang_top10)]

    # Plot top 10 languages per decade
    for language in lang_top10:
        # Create a single dataframe per language
        language_df = lang_df.loc[lang_df["languages"] == language]
        # Create list with the sum of counts per decade per language
        count_list = []
        for start in range(1930, 2020, 10):
            end = start + 10
            count_decade = language_df.loc[(language_df["year"] >= start) & (language_df["year"] < end), "count"].sum()
            count_list.append(count_decade)
        # Make one lineplot per language
        plt.plot(range(1930, 2020, 10), count_list, 'o-', markersize=4, label=language)
    # Create legend for plots
    plt.legend()
    
    # Save plot as png image
    plt.savefig(output_file_name, bbox_inches='tight', pad_inches = 0.2)
    
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