import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
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

df["label"]=pd.qcut(df["score"],labels=[1,2,3],q=3).astype(int)   #converting scores to categories 1,2,3->1(easy),2(medium),3(advance)

df.drop(['excerpt', 'target', 'Excerpt', 'BT_easiness'],axis=1,inplace=True)


print(df.columns)

vectorizer=TfidfVectorizer(max_features=10000,stop_words="english")
X=vectorizer.fit_transform(df["full_text"])

model=LogisticRegression(solver="lbfgs",max_iter=1000)

X_train,X_test,Y_train,Y_test=train_test_split(X,df["label"],test_size=0.2)
model.fit(X_train,Y_train)

print(df.head(10))
print(model.coef_.shape)
print(model.coef_)
print(model.intercept_)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(Y_test, y_pred))
print(classification_report(Y_test, y_pred))
print(df["label"].value_counts())