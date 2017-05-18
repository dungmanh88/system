import pandas
import webbrowser
import os

# Read the dataset into a data table using Pandas
data_table = pandas.read_csv("movie_ratings_data_set.csv")

# Create a web page view of the data for easy viewing
html = data_table[0:100].to_html()

# Save the html to a temporary file
with open("data.html", "w") as f:
    f.write(html)

# Open the web page in our web browser
full_filename = os.path.abspath("data.html")
webbrowser.open("file://{}".format(full_filename))