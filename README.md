# The-Movie-Recommendation-System
This project is a part of my Microsoft Intern Engage 2022
In this I am using python and its libraries such as scikit-learn, pandas etc for Machine Learning.
and for front end I am using flask and HTML, CSS, bootstrap.

# About
This Content Based Filtering Movie Recommender is built on a flask app using Python programming language.
I used the package “scikit-learn”, "pandas", "Numpy" and there I'll be using "Cosine-Similarity", "Vectorization" .
Here, feature extraction methods and distance metrics are utilised to generate recommendations.

# Content based Recommender System
Feature extraction methods such as Bag-of-words vectorises the text data and distance metrics such as
Cosine Similarity computes the similarity between each item by calculating the distance between each vector.

# Cosine Similarity

The distance metric used in this recommender is Cosine Similarity. Cosine Similarity computes the similarity
of items by measuring the cosine of the angle between two vectors projected in a multidimensional vector
With Cosine Similarity, non-binary vector values are taken into consideration during calculation as the values directly
influence the position of the vector. Cosine Similarity focuses on the contents of the items and disregards the size
of the items. Hence, Cosine Similarity is suitable for text documents with different word counts.

# Dataset Link
Movies Dataset - https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv

Credits Dataset - https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv

# How to run this project
1. Create a Virtual Environment 
2. Go to that venv, you can use this command (./env/Scripts/Activate.ps1)
3. Install the requirement.txt file (pip install requirements.txt)
4. Run the flask app (Python .\app.py)



I had deployed once to test my backend =-- https://ms-algo-deep.herokuapp.com (this is not the full app it was only for testing backend)
