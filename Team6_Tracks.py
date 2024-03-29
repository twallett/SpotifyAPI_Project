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
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score, roc_curve
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.model_selection import GridSearchCV
import seaborn as sns
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score



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

#Popularity to nominal ordinal variable: 0-Not popular 0-50, 1-Popular 50-100

sns.countplot(x = 'popularity', data = spotify,palette = "Set2").set(title='Countplot for popularity')

spotify = spotify[spotify['popularity'] != 0]

#%%
#EDA on popular songs 

x = spotify[spotify['popularity'] > 90]

x = x[['name', 'artists', 'popularity']].sort_values('popularity', ascending=False)

x.head(10)

#%%
#EDA on popular songs -> danceability

x = spotify[spotify['popularity'] > 90]

x = x[['name', 'artists', 'popularity','danceability']].sort_values('popularity', ascending=False).sort_values('danceability', ascending=False)

x.head(10)

#%%
#EDA on popular songs -> energy

x = spotify[spotify['popularity'] > 90]

x = x[['name', 'artists', 'popularity','energy']].sort_values('popularity', ascending=False).sort_values('energy', ascending=True)

x.head(10)


#%%
#Dropping songs with 0 popularity given that it will skew the results later on...

spotify['popularity'] = spotify['popularity'].map(lambda x: 0 if x <= 50 else 1 if x <= 100 else np.nan)

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
#Deleting songs whose release year is past 2022
spotify['year'] = spotify['year'].map(lambda x: np.nan if x > 2022 else x)

spotify = spotify.dropna()

#%%
#Dropping columns for EDA and modeling

spotifydf = spotify.drop(columns= ['id',
                                   'duration_ms'])

#%%
spotifydf.info()

#%%[markdown]
# Answering the questions
#
# (EDA) SMART Question: What factors affect the popularity of a song?
#
# Feature Selection: Correlation plot to check for linear relationships 
fig, ax = plt.subplots(figsize = (15,15))

mask1 = np.triu(np.ones_like(spotifydf.corr(), dtype=np.bool))

spotifydfcorr = spotifydf.corr(method='spearman')
sns.heatmap(spotifydfcorr, 
            annot =True, 
            mask=mask1)

plt.title('Spearman Correlation Heatmap of Spotifydf')

#%%
# Spotifydf at a glance
spotifydf.hist(bins = 20, color = 'lightgreen', figsize = (20, 14))

#%%
# EDA on popular and unpopular data over the years

unpopular = spotifydf[spotifydf['popularity'] == 0]

popular = spotifydf[spotifydf['popularity'] == 1]

#%%

fig, axes = plt.subplots(2,3, figsize=(15,10))
axes[1][2].set_visible(False)

axes[1][0].set_position([0.24,0.125,0.228,0.343])
axes[1][1].set_position([0.55,0.125,0.228,0.343])


ax1 = sns.histplot(spotifydf, 
            x="explicit",
            hue="popularity",
            kde=True,
            multiple="stack",
            legend= False,
            ax= axes[0,0])

ax2 = sns.histplot(spotifydf, 
            x="danceability",
            hue="popularity",
            kde=True,
            multiple="stack",
            legend= False,
            ax= axes[0,1])

ax4 = sns.histplot(spotifydf, 
             x="loudness",
             hue="popularity",
             kde=True,
             multiple="stack",
             legend= False,
             ax= axes[0,2])

ax5 = sns.histplot(spotifydf, 
             x="acousticness",
             hue="popularity",
             kde=True,
             multiple="stack",
             legend= False,
             ax= axes[1,0])

ax6 = sns.histplot(spotifydf, 
             x="year",
             hue="popularity",
             kde=True,
             multiple="stack",
             legend= False,
             ax= axes[1,1])

ax1.title.set_text('Histplot Explicit')
ax2.title.set_text('Histplot Danceability')
ax4.title.set_text('Histplot Loudness')
ax5.title.set_text('Histplot Acousticness')
ax6.title.set_text('Histplot Year')

fig.legend(loc = 'right', labels = ['Popular','Not popular'])


#%%
# Explicit songs over the years
fig, axes = plt.subplots(2,2, figsize=(15,10))

ax1 = sns.lineplot(x = 'year',
             y = 'explicit',
             data= spotifydf,
             hue= 'popularity',
             legend=False,
             ax= axes[0,0])

# Danceability songs over the years

ax2 = sns.lineplot(x = 'year',
             y = 'danceability',
             hue= 'popularity',
             legend=False,
             data= spotifydf,
             ax= axes[0,1])

# loudness songs over the years

ax4 = sns.lineplot(x = 'year',
             y = 'loudness',
             hue= 'popularity',
             legend=False,
             data= spotifydf,
             ax= axes[1,0])

# Accousticness songs over the years

ax5 = sns.lineplot(x = 'year',
             y = 'acousticness',
             hue= 'popularity',
             legend=False,
             data= spotifydf,
             ax= axes[1,1])

ax1.title.set_text('Explicit vs Year')
ax2.title.set_text('Danceability vs Year')
ax4.title.set_text('Loudness vs Year')
ax5.title.set_text('Acousticness vs Year')

fig.legend(loc = (0.89,0.5), labels = ['Not popular', 'NP 95% Conf. Int.','Popular','P 95% Conf. Int.'])

#%%
#Distribution of variables of interest



#%%
# (Modeling) SMART Question: Based on the features, will a song be popular or not?

# %%
# Logistic regression

x_spotifydf = spotifydf[['explicit',
                         'danceability',
                         'loudness',
                         'acousticness',
                         'year']]

y_spotifydf = spotifydf[['popularity']]

x_train, x_test, y_train, y_test = train_test_split(x_spotifydf, y_spotifydf, test_size= 0.2, random_state= 321)

smo = SMOTE(random_state = 2)

x_train_res, y_train_res = smo.fit_resample(x_train, y_train)

modelLogistic = LogisticRegression()

modelLogistic.fit(x_train_res, y_train_res)

y_predLogistic = modelLogistic.predict(x_test)

print(modelLogistic.score(x_train_res, y_train_res))
print(modelLogistic.score(x_test, y_test))

print(classification_report(y_test, y_predLogistic))
print(confusion_matrix(y_test, y_predLogistic))

#%%
#Cross validation

cv_logistic = cross_val_score(modelLogistic, x_train_res, y_train_res, cv = 10)

print(cv_logistic)
print(cv_logistic.mean())

#%%
# ROC and AUC 

ns_probs = [0 for _ in range(len(y_test))]

lr_probs = modelLogistic.predict_proba(x_test)

lr_probs = lr_probs[:, 1]

ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)

print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Logistic: ROC AUC=%.3f' % (lr_auc))

ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)

plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC: Logistic Regression')
plt.legend()

#%%
#Tentative: Statsmodel

smotelogistic = x_train_res.merge(y_train_res, left_index=True, right_index=True)

from statsmodels.formula.api import glm

modelGLM = glm(formula= 'popularity ~ danceability + C(explicit) + loudness + acousticness + year', data= smotelogistic, family=sm.families.Binomial())

modelGLM = modelGLM.fit()

print( modelGLM.summary())

#%%
fig, ax = plt.subplots(figsize = (7,7))

sns.countplot(x = 'popularity', data = y_train_res,palette = "Set2", ax=ax).set(title='Countplot for popularity with SMOTE')

ax.set_xticklabels(['Not popular', 'Popular'])


#%%
# K-Nearest Neighbors 

#%%
#Data pre-processing

X=spotifydf.loc[:,['danceability', 'energy', 'loudness', 'speechiness', 'acousticness','liveness', 'valence', 'tempo', 'duration_min', 'year']]

y=spotifydf["popularity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

#%%
#Modelling

b=pd.DataFrame(columns=['K', 'Accuracy'])
for i in range(1,21):
    knn = KNeighborsClassifier(n_neighbors = i)
    knn.fit(X_train,y_train)
    knn.predict(X_test)
    print(i)
    print(knn.score(X_test, y_test))
    temp=knn.score(X_test, y_test)
    #new_row = {'K':i, 'Accuracy':temp}
    #b = b.append(new_row, ignore_index=True)
    b.loc[i]=[i,temp]
    #b.update({i:knn.score(X_test, y_test)})
    print("   ")

#%%
plt.plot(b['K'], b['Accuracy'])
plt.xlabel('K') 
plt.ylabel('Accuracy') 
plt.title("Accuracy with different K")
plt.xticks(range(0, 21))
plt.show() 

#%%
#KNN = 9  

knn_best = KNeighborsClassifier(n_neighbors=9)

knn_best.fit(X_train, y_train)

print(cross_val_score(knn_best, X_train, y_train, cv=10))

y_pred = knn.predict(X_test)

#%%
#Evaluation Metrics

print(" ")
print("The Classification Report")
print(classification_report(y_test, y_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(y_test,y_pred))
print(" ")
print("Precision Score")
print(precision_score(y_test, y_pred))
print(" ")
print("Recall Score")
print(recall_score(y_test, y_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(y_test, y_pred))


#%%
#SMOTE

X=spotifydf.loc[:,['danceability', 'energy', 'loudness', 'speechiness', 'acousticness','liveness', 'valence', 'tempo', 'duration_min', 'year']]

y=spotifydf["popularity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

smo = SMOTE(random_state = 2)

x_train_res, y_train_res = smo.fit_resample(X_train, y_train)

#%%
#KNN SMOTE

knn_smo = KNeighborsClassifier(n_neighbors=9)

knn_smo.fit(x_train_res,y_train_res)

knn_smo_pred = knn_smo.predict(X_test)

print(cross_val_score(knn_smo, x_train_res, y_train_res, cv=10))

#%%
#Evaluation metrics SMOTE

print(" ")
print("The Classification Report")
print(classification_report(y_test, knn_smo_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(y_test,knn_smo_pred))
print(" ")
print("Precision Score")
print(precision_score(y_test, knn_smo_pred))
print(" ")
print("Recall Score")
print(recall_score(y_test, knn_smo_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(y_test, knn_smo_pred))


#%%
# Random Forest 

# %%
spotifydf.columns

# %%
x_spotifydf = spotifydf.loc[:,["explicit","danceability","energy","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","duration_min","year","month"]]

y_spotifydf = spotifydf[['popularity']]

X_train, X_test, Y_train, Y_test = train_test_split(x_spotifydf, y_spotifydf, test_size= 0.2, random_state= 321)

#%%

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn import metrics


#%%
# RF without feature selection
rf_best = RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 100, max_depth=5)
rf_best.fit(X_train, Y_train)
y_pred=rf_best.predict(X_test)
#%%
import seaborn as sns
plt.figure(figsize=(5, 7))
ax = sns.distplot(Y_test, hist=False, color="r", label="Actual Value")
sns.distplot(y_pred, hist=False, color="b", label="Fitted Values" , ax=ax)
plt.title('Actual vs Fitted Values for Popularity')
plt.show()
plt.close()
#%%
#Accuracy

print(" ")
print("The Classification Report")
print(classification_report(Y_test, y_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(Y_test,y_pred))
print(" ")
print("Precision Score")
print(precision_score(Y_test, y_pred))
print(" ")
print("Recall Score")
print(recall_score(Y_test, y_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(Y_test, y_pred))

#%%
#Data Visualization
# display = PrecisionRecallDisplay.from_estimator(
#     rf_best, X_test, Y_test)
# _ = display.ax_.set_title("2-class Precision-Recall curve")

# fpr, tpr, _ = metrics.roc_curve(Y_test,  y_pred)
# auc = metrics.roc_auc_score(Y_test, y_pred)
# plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
# plt.legend(loc=4)
# plt.show()

lr_fpr, lr_tpr, _ = roc_curve(Y_test, y_pred)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Random Forest')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC: Random Forest')
plt.legend()


#%% 
#Using SMote, RF_without FE
X_train, X_test, Y_train, Y_test = train_test_split(x_spotifydf, y_spotifydf, test_size= 0.2, random_state= 321)
smo = SMOTE(random_state = 2)
x_train_res, y_train_res = smo.fit_resample(X_train, Y_train)

#%%
rf_best = RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 100, max_depth=5)
rf_best.fit(x_train_res, y_train_res)
y_pred=rf_best.predict(X_test)

#%%
#Accuracy

print(" ")
print("The Classification Report")
print(classification_report(Y_test, y_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(Y_test,y_pred))
print(" ")
print("Precision Score")
print(precision_score(Y_test, y_pred))
print(" ")
print("Recall Score")
print(recall_score(Y_test, y_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(Y_test, y_pred))

#%%
#Data Visualization
# display = PrecisionRecallDisplay.from_estimator(
#     rf_best, X_test, Y_test)
# _ = display.ax_.set_title("2-class Precision-Recall curve")

# fpr, tpr, _ = metrics.roc_curve(Y_test,  y_pred)
# auc = metrics.roc_auc_score(Y_test, y_pred)
# plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
# plt.legend(loc=4)
# plt.show()

lr_fpr, lr_tpr, _ = roc_curve(Y_test, y_pred)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Random Forest')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC: Random Forest')
plt.legend()

import seaborn as sns
plt.figure(figsize=(5, 7))
ax = sns.distplot(Y_test, hist=False, color="r", label="Actual Value")
sns.distplot(y_pred, hist=False, color="b", label="Fitted Values" , ax=ax)
plt.title('Actual vs Fitted Values for Popularity')
plt.show()
plt.close()

#%%
# Feature Selection
sel = SelectFromModel(RandomForestClassifier(n_estimators = 100))
sel.fit(X_train, Y_train)

print(sel.get_support())

selected_feat= X_train.columns[(sel.get_support())]
print(len(selected_feat))

print(selected_feat)

#%%
#Based on Feature selection creating new training data
x_spotifydf1 = spotifydf.loc[:,['danceability', 'energy', 'loudness', 'speechiness', 'acousticness','liveness', 'valence', 'tempo', 'duration_min', 'year']]

y_spotifydf1 = spotifydf[['popularity']]

X_train, X_test, Y_train, Y_test = train_test_split(x_spotifydf1, y_spotifydf1, test_size= 0.2, random_state= 321)

#%%
#RF using GridSearchCV

##### GridSearchCV CODES TAKE OVER 3 HOURS TO RUN ########
# rfc=RandomForestClassifier(random_state=42)

# param_grid = { 
#     'n_estimators': [100,200,300,400,500],
#     'max_features': ['auto', 'sqrt', 'log2'],
#     'max_depth' : [4,5,6,7,8,10,14,20],
#     'criterion' :['gini', 'entropy',"log_loss"],
#     'bootstrap' :[True,False],
#     'oob_score' :[True,False]
# }

# CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
# CV_rfc.fit(X_train, Y_train)


# print(CV_rfc.best_params_)
###### HENCE, HERE'S A DESCRIPTION OF THE RESULTS TO SAVE TIME ##########

print(f"The best hyperparameters for RF using GridSearchCV were: max_features='auto', n_estimators= 200, max_depth=8, criterion='gini', bootstrap=True, and oob_score=True.")


#%%
#Training RF on best parameters
rf_best = RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 200, max_depth=8, criterion='gini', bootstrap=True, oob_score=True)
rf_best.fit(X_train, Y_train)
y_pred=rf_best.predict(X_test)
print(accuracy_score(Y_test,y_pred))

#%%
#Accuracy

print(" ")
print("The Classification Report")
print(classification_report(Y_test, y_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(Y_test,y_pred))
print(" ")
print("Precision Score")
print(precision_score(Y_test, y_pred))
print(" ")
print("Recall Score")
print(recall_score(Y_test, y_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(Y_test, y_pred))

#%%
#Data Visualization
# display = PrecisionRecallDisplay.from_estimator(
#     rf_best, X_test, Y_test)
# _ = display.ax_.set_title("2-class Precision-Recall curve")

# fpr, tpr, _ = metrics.roc_curve(Y_test,  y_pred)
# auc = metrics.roc_auc_score(Y_test, y_pred)
# plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
# plt.legend(loc=4)
# plt.show()

lr_fpr, lr_tpr, _ = roc_curve(Y_test, y_pred)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Random Forest')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC: Random Forest')
plt.legend()
# Visualization of Result
import seaborn as sns
plt.figure(figsize=(5, 7))
ax = sns.distplot(Y_test, hist=False, color="r", label="Actual Value")
sns.distplot(y_pred, hist=False, color="b", label="Fitted Values" , ax=ax)
plt.title('Actual vs Fitted Values for Popularity')
plt.show()
plt.close()

#%%
# SMOTE_RF_with FE
x_spotifydf1 = spotifydf.loc[:,['danceability', 'energy', 'loudness', 'speechiness', 'acousticness','liveness', 'valence', 'tempo', 'duration_min', 'year']]
y_spotifydf1 = spotifydf[['popularity']]
X_train, X_test, Y_train, Y_test = train_test_split(x_spotifydf1, y_spotifydf1, test_size= 0.2, random_state= 321)
smo = SMOTE(random_state = 2)
x_train_res, y_train_res = smo.fit_resample(X_train, Y_train)

rf_best = RandomForestClassifier(random_state=42, max_features='auto', n_estimators= 200, max_depth=8, criterion='gini', bootstrap=True, oob_score=True)
rf_best.fit(x_train_res, y_train_res)
y_pred=rf_best.predict(X_test)
print(accuracy_score(Y_test,y_pred))

#%%
#Accuracy

print(" ")
print("The Classification Report")
print(classification_report(Y_test, y_pred))
print(" ")
print("Accuracy is ")
print(accuracy_score(Y_test,y_pred))
print(" ")
print("Precision Score")
print(precision_score(Y_test, y_pred))
print(" ")
print("Recall Score")
print(recall_score(Y_test, y_pred))
print(" ")
print("ROC_AUC Score")
print(roc_auc_score(Y_test, y_pred))

#%%
#Data Visualization
# display = PrecisionRecallDisplay.from_estimator(
#     rf_best, X_test, Y_test)
# _ = display.ax_.set_title("2-class Precision-Recall curve")

# fpr, tpr, _ = metrics.roc_curve(Y_test,  y_pred)
# auc = metrics.roc_auc_score(Y_test, y_pred)
# plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
# plt.legend(loc=4)
# plt.show()

lr_fpr, lr_tpr, _ = roc_curve(Y_test, y_pred)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Random Forest')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC: Random Forest')
plt.legend()
# Visualization of Result

import seaborn as sns
plt.figure(figsize=(5, 7))
ax = sns.distplot(Y_test, hist=False, color="r", label="Actual Value")
sns.distplot(y_pred, hist=False, color="b", label="Fitted Values" , ax=ax)
plt.title('Actual vs Fitted Values for Popularity')
plt.show()
plt.close()



