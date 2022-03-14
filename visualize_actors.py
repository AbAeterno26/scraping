# visualize_actors.py
# Name: Sarah Blok
# Student number: 11867310
# Purpose: Demonstrates how to create a plot
# GitHub link: https://github.com/AbAeterno26/scraping.git

import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # Read csv file
    movies_df = pd.read_csv(input_file_name)
    
    # Split the column actors at the semicolon to get each individual actor
    movies_df["actors"] = movies_df["actors"].str.split(";")
    
    # Exlode the actors column to transform the list into separate rows for each actor
    movies_df = movies_df.explode("actors")
    
    # Find the top 50 actors who starred in the most movies
    movies_df["count"] = movies_df.groupby(["actors"]).actors.transform("count")
    movies_df = movies_df.sort_values(by="count", ascending=False).drop_duplicates(["actors"]).head(50)
    
    # Find maximum value and set unique color
    max_value = movies_df["count"].max()
    colors = ['r' if actors_count == max_value else 'b' for actors_count in movies_df["count"]]
     
    # Plot top 50 actors with the most appearances in dataset
    movies_plot = movies_df.plot.bar("actors", "count", color=colors, title="Top 50 actors", ylabel="Number of movies", xlabel="Actor",
                                    figsize=(10, 6), legend=False, grid=True)
    
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