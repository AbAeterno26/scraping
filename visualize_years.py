# visualize_years.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to create a plot
# GitHub link: https://github.com/AbAeterno26/scraping.git

import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # Read csv file
    movies_df = pd.read_csv(input_file_name)
    
    # Find the average rating for top 5 movies per year
    movies_df = movies_df.groupby("year")["rating"].mean().reset_index()

    # Find maximum value and set unique color
    max_value = movies_df["rating"].max()
    colors = ['r' if rating == max_value else 'b' for rating in movies_df["rating"]]
    
    # Plot average rating for top 5 movies per year
    movies_plot = movies_df.plot.bar("year", "rating", title="Top 5 movies per year", ylabel="Rating", xlabel="Year", 
                                     figsize=(15,8), legend=False, grid=True, color=colors,
                                     ylim=[int(movies_df["rating"].min()), int(movies_df["rating"].max() + 0.5)])
        
    # Show label on x axis for every 10 years
    for i,label in enumerate(movies_plot.xaxis.get_ticklabels()):
        if i % 10 != 0:
                label.set_visible(False)
    
    # Create figure from plot and save it as png image
    movies_plot = movies_plot.get_figure().savefig(output_file_name, bbox_inches='tight', pad_inches = 0.2)

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