import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
from sklearn.metrics import r2_score,mean_absolute_error, mean_squared_error
#In both:
#Higher score = easier text.
#Lower score = harder text

df1=pd.read_csv("train1.csv")
df2=pd.read_csv("train2.csv")

df1=df1[["excerpt","target"]]
df2=df2[["Excerpt","BT_easiness"]]
df=pd.concat([df1,df2],axis=0,ignore_index=True)
del df1,df2

df["full_text"]=df["excerpt"].fillna("") + " " + df["Excerpt"].fillna("")
#normalization
target_mean=df["target"].mean()
target_std=df["target"].std()
df["target"]=(df["target"]-target_mean)/target_std
bt_mean=df["BT_easiness"].mean()
bt_std=df["BT_easiness"].std()
df["BT_easiness"]=(df["BT_easiness"]-bt_mean)/bt_std

df["score"] = np.where(df["target"].isna().values,df["BT_easiness"] , df["target"] )# colud also use->df["target"].fillna(df["BT_easiness"])   #If target is not NaN → combined_score = target ;   If target is NaN → combined_score = BT_easiness

df.drop(['excerpt', 'target', 'Excerpt', 'BT_easiness'],axis=1,inplace=True)


print(df.columns)
'''
vectorizer=TfidfVectorizer(max_features=10000,stop_words="english")
X=vectorizer.fit_transform(df["full_text"])

model=LinearRegression()

X_train,X_test,Y_train,Y_test=train_test_split(X,df["score"],test_size=0.2, random_state=42)
model.fit(X_train,Y_train)

print(df.head(10))
print(model.coef_.shape)
print(model.coef_)
print(model.intercept_)
y_pred = model.predict(X_test)  
print(model.score(X_test,Y_test))  # Returns R² score


mae = mean_absolute_error(Y_test, y_pred)
rmse = np.sqrt(mean_squared_error(Y_test, y_pred))

print("MAE:", mae)
print("RMSE:", rmse) '''

X_train,X_test,Y_train,Y_test=train_test_split(df["full_text"],df["score"],test_size=0.2, random_state=42)

#buining pipeline
pipeline=Pipeline([('tfidf',TfidfVectorizer(max_features=10000,stop_words="english")),
                        ('model',LinearRegression())])

# Train on your full_text strings and score targets
pipeline.fit(X_train,Y_train)

pred = pipeline.predict(X_test)
# Save once
joblib.dump(pipeline, 'text_scorer_pipeline.pkl')