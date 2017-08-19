import os
import pandas
import webbrowser

data_table = pandas.read_csv("Ex_Files_ML_EssT_Recommendations/Exercise Files/Chapter 4/movie_ratings_data_set.csv")
html = data_table[0:10].to_html()

with open("data.html", "w") as f:
    f.write(html)
full_name = os.path.abspath("data.html")
webbrowser.open("file://{}".format(full_name))
