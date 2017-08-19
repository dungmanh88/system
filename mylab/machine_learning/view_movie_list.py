import pandas
import os
import webbrowser

data_table = pandas.read_csv("Ex_Files_ML_EssT_Recommendations/Exercise Files/Chapter 4/movies.csv", index_col="movie_id")
html = data_table.to_html()
with open("movies_list.html", "w") as f:
    f.write(html)

full_name = os.path.abspath("movies_list.html")
webbrowser.open("file://{}".format(full_name))
