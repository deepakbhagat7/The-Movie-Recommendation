import pandas as pd
from flask import Flask,  render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import requests

#importing movies's dataset as well as credits dataset
credits=pd.read_csv('tmdb_5000_credits.csv')
movies=pd.read_csv('tmdb_5000_movies.csv')
# merging both in single dataframe with specific columns
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 
# Explortary Data Analysis ------>
movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L

movies['cast'] = movies['cast'].apply(convert)
movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 

movies['crew'] = movies['crew'].apply(fetch_director)

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

new['tags'] = new['tags'].apply(lambda x: " ".join(x))
# Explortary Data Analysis Finished ------>

# Now, we will stopwords in vectorization (stopwords - a, the, from, after etc)
cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()
# calculating cosine similarity - angular distance
similarity = cosine_similarity(vector)
new[new['title'] == 'The Lego Movie'].index[0]

# fething posters from tmdb API 
def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=f0b1c6b7d4e29ee7c05c8f77b7075fa3&language=en-US".format(movie_id)
     data = requests.get(url)
     data = data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path


def get_recommendation(movie):

   if movie not in movies['title'].values:
          return ('This movie is not in our database.\nPlease check if you spelled it correct using camel casing')
   else:

     index = new[new['title'] == movie].index[0]
     #sorting in descending order of simalarity scores
     distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
     recommended_movie_names = []
     #fetching posters of top 13 matches
     for i in distances[0:13]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
     return recommended_movie_names




def get_poster(movie):
    
  if movie not in movies['title'].values:
          return ('This movie is not in our database.\nPlease check if you spelled it correct using camel casing')
  else:  
     index = new[new['title'] == movie].index[0]
     #sorting in descending order of simalarity scores
     distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
     recommended_movie_posters = []
     #fetching posters of top 13 matches
     for i in distances[0:13]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
     return recommended_movie_posters 


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')
    

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')
    recommended_movies = get_recommendation(movie)
    poster = get_poster(movie)
    if type(recommended_movies)==type('string'):
        return render_template('recommend.html',movie=movie, poster=poster ,recommended_movies=recommended_movies,movies_input='not_in_database')
    else:
        return render_template('recommend.html',movie=movie, poster=poster, recommended_movies=recommended_movies,movies_input='list_of_movies')



if __name__=="__main__":
    app.run(debug=True)




