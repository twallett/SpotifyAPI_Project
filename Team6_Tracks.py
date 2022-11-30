#%%[markdown]
## Getting to know the variables in the `Spotify` dataset
#
# According to Spotify's web developer API on ['Get Tracks'](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track) data:
#
# * name : (STR) The name of the track.
#
# * popularity: (INT) The popularity of the track. The value will be between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity. Note: the popularity value may lag actual popularity by a few days: the value is not updated in real time.
#
# * explicit: (BOOLEAN) Whether or not the track has explicit lyrics ( true = yes it does; false = no it does not OR unknown).
#
# * artists: (ARRAY) The artists who performed the track. Each artist object includes a link in href to more detailed information about the artist.
#
# * release_date: (STR) The date the album was first released.
#
# According to Spotify's web developer API on ['Get Tracks Audio Features'](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
#
# * danceability: (FLOAT) Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
#
# * energy: (FLOAT) Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
#
# * key: (INT) The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
#
# * loudness: (FLOAT) The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
#
# * mode: (INT) Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
#
# * speechiness: (FLOAT) Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
#
# * acousticness: (FLOAT) A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
#
# * instrumentalness: (FLOAT) Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
#
# * liveness: (FLOAT) Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
#
# * valence: (FLOAT) A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
#
# * tempo: (FLOAT) The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
#
# * duration_ms: (INT) Duraiton of the song in miliseconds.

#%%
#Importing modules 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
#%%
#Importing dataset 

spotify = pd.read_csv('tracks.csv')
# %%
print(spotify.head())
print(spotify.info())
print(spotify.shape)

#%% 
#Cleaning the data set 

# Checking for Null values
spotify.isna().sum()

#Dropping null values
spotify.dropna(axis=0,inplace=True)

# %%
#Reformatting variables of interest

#Popularity to nominal ordinal variable: 1- 0 to 25, 2- 25 to 50, 3- 50-75 and 4- 75-100

sns.countplot(x = 'popularity', data = spotify,palette = "Set2").set(title='Countplot for popularity')

#%%
#Dropping songs with 0 popularity given that it will skew the results later on...
spotify['popularity'] = spotify['popularity'].map(lambda x: np.nan if x == 0 else 1 if x <= 25 else 2 if x <= 50 else 3 if x <= 75 else 4 if x <= 100 else np.nan)

spotify = spotify.dropna()

sns.countplot(x = 'popularity', data = spotify,palette = "Set2").set(title='Countplot for popularity')

#%%
#Reformating duration_ms to duration in minutes 

spotify['duration_min'] = round(spotify['duration_ms']* 1.6667e-5, 2)


#%%
#Reformating release_date

spotify['release_date'] = pd.to_datetime(spotify['release_date'])

spotify["year"] = spotify["release_date"].dt.year

spotify["month"] = spotify["release_date"].dt.month

#%%
#Dropping columns for EDA and modeling

spotifydf = spotify.drop(columns= ['id',
                                   'duration_ms'])


#%%
#Answering the questions

# (EDA) SMART Question: What factors make a song danceable? 

# (EDA) SMART Question: Does loudness influence the energy of a song?

# (EDA) SMART Question: What factors affect the popularity of a song?


#%%
# (Modeling) SMART Question: Based on the features, will a song be popular or not?

fig, ax = plt.subplots(figsize = (15,15))

mask1 = np.triu(np.ones_like(spotifydf.corr(), dtype=np.bool))

spotifycorr = spotifydf.corr()
sns.heatmap(spotifycorr, 
            annot =True, 
            mask=mask1)

plt.title('Correlation plot of Spotifydf')

# %%
# Logistic regression




#%%
# K-Nearest Neighbors 


#%%
# Random Forest 
